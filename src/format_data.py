import json
import argparse
import jsonlines

from tqdm import tqdm


def test(data):
    print(json.dumps(json.loads(data), ensure_ascii=False, indent=4))

def convert(data: dict, tp: str):
    instruction = ''
    ipt = ''
    opt = ''
    history = []

    if tp == 'ner' or tp == 'text_classification':
        instruction = data['instruction']
        ipt = data['input']
        opt = data['output']
    elif tp == 'relation_extract' or tp == 'qa':
        instruction = data['question']
        opt = data['answer']
    elif tp == 'multi_choice':
        instruction = data['question'] + '\n' + '\n'.join(data['options'])
        opt = data['correct_answer']
    elif tp == 'dialog':
        history = [[turn['human'], turn['assistant']] for turn in data]
        instruction = history[-1][0]
        opt = history[-1][1]
        history = history[:-1]

    return {
        'instruction': instruction,
        'input': ipt,
        'output': opt,
        'history': history,
        'task_type': tp
    }

def extract(data: str, tp: str):
    if tp == 'dialog':
        results = [json.loads(data)]
    else:
        results = json.loads(data)
    return [convert(i, tp) for i in results]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_pth", "-i", type=str, default='step6.jsonl')
    parser.add_argument("--output_pth", "-o", type=str, default='step7.json')
    args = parser.parse_args()
    
    with jsonlines.open(args.input_pth, mode='r') as reader:
        lines = list(reader)
    
    datas = []
    for i, line in tqdm(enumerate(lines), total=len(lines), ncols=100):
        try:
            tp = line['task_type']
            data = line['data']
            # data = data.replace('\~', '~')
            if len(data) > 20:
                datas.extend(extract(data, tp))
            elif len(data) > 0:
                print('too short data.')
        except Exception as e:
            print(f"line {i}: {e}")
    
    with open(args.output_pth, 'w', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)
    
    print(f"Generate {len(datas)} samples total.")
