import json, urllib.request, urllib.parse, urllib.error, pathlib, concurrent.futures, time
import sys
ROOT=pathlib.Path(sys.argv[1])
AUTHORS=json.loads((ROOT / 'data/supervisors.json').read_text(encoding='utf-8'))
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CENA-PPG-research/1.0'}),timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if attempt==2: raise
            if e.code==429:
                time.sleep(min(60,int(e.headers.get('Retry-After','60'))))
            else:time.sleep(2)
        except Exception:
            if attempt==2: raise
            time.sleep(2)
def author_search(item):
    dest=ROOT/'data/raw'/('author_'+str(AUTHORS.index(item))+'.json');dest.parent.mkdir(exist_ok=True)
    if dest.exists(): data=json.loads(dest.read_text())
    else:
        data=get('https://api.openalex.org/authors?'+urllib.parse.urlencode({'search':item['query'],'per-page':10}))
        dest.write_text(json.dumps(data,ensure_ascii=False))
    return {'name':item['name'],'candidates':[{'id':a['id'],'name':a['display_name'],'orcid':a.get('orcid'),'works_count':a['works_count'],'institutions':[i['display_name'] for i in (a.get('last_known_institutions') or [])],'topics':[t['display_name'] for t in (a.get('topics') or [])[:4]]} for a in data['results'][:6]]}
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        out=list(ex.map(author_search,AUTHORS))
    (ROOT/'data/candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps(out,ensure_ascii=False,indent=2))
