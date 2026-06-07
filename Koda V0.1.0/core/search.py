def filter_snippets(items,q):
    q=q.lower()
    return [i for i in items if q in (i['title']+' '+i['tags']+' '+i['code']).lower()]
