# coding=utf-8

import time
import json
import random
import argparse
import jsonlines

from api import ernie
from tqdm import tqdm
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from prompt_template import ner_prompt, text_classification_prompt, relation_extract_prompt, qa_prompt, multi_choice_prompt, dialog_prompt


prompts = [ner_prompt, text_classification_prompt, relation_extract_prompt, qa_prompt, multi_choice_prompt, dialog_prompt]
task_type_list = ["ner", "text_classification", "relation_extract", "qa", "multi_choice", "dialog"]

def work(line, model):
    response = ''
    num = random.randint(0, 5)
    task_type = task_type_list[num]
    prompt = prompts[num]
    knowledge = line['knowledge'].split('### 整合结果')[-1]
    prompt = prompt.replace("```{entity_knowledge}```", knowledge)

    if len(knowledge) > 20:
        for t in range(3):
            if 'output' in locals():
                del output
            try:
                output = ernie(model, prompt)
                output = output.replace('\~', '~')
                # check whether output is json
                json.loads(output)
                response = output
                break
            except Exception as e:
                print(f"try {t} failed: {e}")
                if 'output' in locals():
                    print(f"invalid json output:\n{output}")
                time.sleep(10)
    elif len(knowledge) > 0:
        print('too short knowledge.')

    line['task_type'] = task_type
    line["data"] = response
    return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, default='ernie-4.5-turbo-32k')
    parser.add_argument("--input_pth", "-i", type=str, default='step5.jsonl')
    parser.add_argument("--output_pth", "-o", type=str, default='step6.jsonl')
    args = parser.parse_args()
    
    with jsonlines.open(args.input_pth, mode='r') as reader:
        lines = list(reader)
    
    work = partial(work, model=args.model)
    
    start_time = time.time()
    
    # average 2k tokens per request 2 requests per minute
    with ThreadPoolExecutor(max_workers=60) as executor:
        results = executor.map(work, lines)
        with jsonlines.open(args.output_pth, mode='a') as writer:
            for result in tqdm(results, total=len(lines), ncols=100):
                writer.write(result)
                writer._fp.flush()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f}s")
