import json
import requests

from openai import OpenAI


def ernie(model, prompt, temperature=0.6, web_search_enable=False, response_format_type='text'):
    url = "https://qianfan.baidubce.com/v2/chat/completions"
    
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in the medical field."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 8192, # 最大输出token数
        "max_completion_tokens": 2048,  # maximum for ernie-3.5-8k
        "web_search": {
            "enable": web_search_enable,
            "enable_citation": False,
            "enable_trace": False,
        },
        "response_format": {
            "type": response_format_type
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['choices'][0]['message']['content']

client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxxxxxxxxx",
    base_url="https://api.chatanywhere.tech/v1"
)

def gpt(model, prompt, temperature=0.6):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in the medical field."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    
    return response.choices[0].message.content
