import time
import argparse
import jsonlines

from api import ernie
from tqdm import tqdm
from functools import partial
from prompt_template import check_consistency
from concurrent.futures import ThreadPoolExecutor


def work(line, model):
    response = ''
    graph_knowledge = line['graph_knowledge']
    retrival_knowledge = line['retrival_knowledge']
    prompt = check_consistency.format(graph_know=graph_knowledge, retrival_know=retrival_knowledge)
    
    if len(graph_knowledge) > 20 and len(retrival_knowledge) > 20:
        for t in range(3):
            try:
                output = ernie(model, prompt)
                # check output
                assert output.count('### 整合结果') == 1, 'format error'
                response = output
                break
            except Exception as e:
                print(f"try {t} failed: {e}")
                time.sleep(10)
    elif len(graph_knowledge) > 0 and len(retrival_knowledge) > 0:
        print('too short graph knowledge or retrival knowledge.')

    line['knowledge'] = response
    return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, default='ernie-4.5-turbo-32k')
    parser.add_argument("--input_pth", "-i", type=str, default='step4.jsonl')
    parser.add_argument("--output_pth", "-o", type=str, default='step5.jsonl')
    args = parser.parse_args()
    
    with jsonlines.open(args.input_pth, mode='r') as reader:
        lines = list(reader)
    
    work = partial(work, model=args.model)
    
    start_time = time.time()
    
    # average 3k tokens per request 1.2 requests per minute
    with ThreadPoolExecutor(max_workers=80) as executor:
        results = executor.map(work, lines)
        with jsonlines.open(args.output_pth, mode='a') as writer:
            for result in tqdm(results, total=len(lines), ncols=100):
                writer.write(result)
                writer._fp.flush()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f}s")
