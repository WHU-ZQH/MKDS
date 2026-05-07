import json
import math
import random
import jsonlines

from tqdm import tqdm


def remove_NaN(obj):
    if isinstance(obj, dict):
        return {k: remove_NaN(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_NaN(item) for item in obj if not (isinstance(item, float) and math.isnan(item))]
    else:
        return obj

def deduplicate(obj):
    if isinstance(obj, dict):
        return {k: deduplicate(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return list(set(obj))
    else:
        return obj

if __name__ == "__main__":
    with open(r"data\segment.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 去除 NaN 值
    result = [remove_NaN(item) for item in tqdm(data, desc="remove NaN", ncols=100)]
    with open(r"data\step1.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    # 列表去重
    result = [deduplicate(item) for item in tqdm(result, desc="deduplicate", ncols=100)]
    with open(r"data\step2.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    # 封装
    outs = []
    for item in tqdm(result, desc="to string", ncols=100):
        for k, v in item.items():
            if k not in ('ID', 'KG_ID'):
                if "英文名称" in v:
                    assert len(v['英文名称']) > 0, k
                    # if len(v['英文名称']) > 1:
                    #     print(f"{k}: {v['英文名称']}")
                    k = f"{k}（{v['英文名称'][0]}）"
                outs.append({
                    "name": k,
                    "graph_knowledge": json.dumps(v, ensure_ascii=False),
                })
    
    random.shuffle(outs)
    with jsonlines.open(r'data\step3-random.jsonl', mode='w') as writer:
        writer.write_all(outs)
