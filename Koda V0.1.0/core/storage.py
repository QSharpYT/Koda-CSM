import json, os
DB='data/snippets.json'

def load_snippets():
    if not os.path.exists(DB): return []
    with open(DB,'r',encoding='utf-8') as f: return json.load(f)

def save_snippets(data):
    with open(DB,'w',encoding='utf-8') as f: json.dump(data,f,indent=2)
