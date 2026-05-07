import time
import argparse
import jsonlines

from api import ernie
from tqdm import tqdm
from functools import partial
from prompt_template import get_llm_knowledge
from concurrent.futures import ThreadPoolExecutor


def web_chat(line, model):
    response = ''
    prompt = get_llm_knowledge.format(line['name'])
    
    for t in range(3):
        try:
            response = ernie(model, prompt, web_search_enable=True)
            break
        except Exception as e:
            print(f"try {t} failed: {e}")
            time.sleep(10)
    
    line["retrival_knowledge"] = response
    return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, default='ernie-4.5-turbo-32k')
    parser.add_argument("--start", "-s", type=int, default=0)
    parser.add_argument("--end", "-e", type=int, default=100)
    parser.add_argument("--input_pth", "-i", type=str, default='data\step3-random.jsonl')
    parser.add_argument("--output_pth", "-o", type=str, default='step4.jsonl')
    args = parser.parse_args()

    print(f"generate [{args.start}, {args.end})")
    with jsonlines.open(args.input_pth, mode='r') as reader:
        lines = list(reader)[args.start:args.end]
    
    web_chat = partial(web_chat, model=args.model)
    
    start_time = time.time()
    
    # ernie-4.5-turbo-32k TPM 400000    average 6k tokens per request   1 request per minute
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(web_chat, lines)
        with jsonlines.open(args.output_pth, mode='a') as writer:
            for result in tqdm(results, total=len(lines), ncols=100):
                writer.write(result)
                writer._fp.flush()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f}s")
