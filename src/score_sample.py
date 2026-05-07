import time
import json
import argparse
import jsonlines

from api import ernie
from tqdm import tqdm
from functools import partial
from prompt_template import score
from concurrent.futures import ThreadPoolExecutor


def work(line, model):
    response = ''
    question = ''
    if line['history']:
        for q, a in line['history']:
            question += f"问：{q}\n答：{a}\n"
        question += '问：'
    question += line['instruction'] + line['input']

    prompt = score.replace('```{question}```', question).replace('```{answer}```', line['output'])
    
    for t in range(3):
        if 'output' in locals():
            del output
        try:
            output = ernie(model, prompt, temperature=0.1, response_format_type='json_object')
            # check whether output is json
            json.loads(output)
            response = output
            break
        except Exception as e:
            print(f"try {t} failed: {e}")
            if 'output' in locals():
                print(f"invalid json output:\n{output}")
            time.sleep(10)
    
    line["score"] = response
    return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, default='ernie-4.5-turbo-32k')
    parser.add_argument("--input_pth", "-i", type=str, default='step7.json')
    parser.add_argument("--output_pth", "-o", type=str, default='step8.jsonl')
    args = parser.parse_args()
    
    with open(args.input_pth, mode='r', encoding='utf-8') as f:
        lines = json.load(f)
    
    work = partial(work, model=args.model)
    
    start_time = time.time()
    
    # average 1k tokens per request 10 requests per minute
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(work, lines)
        with jsonlines.open(args.output_pth, mode='a') as writer:
            for result in tqdm(results, total=len(lines), ncols=100):
                writer.write(result)
                writer._fp.flush()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f}s")
