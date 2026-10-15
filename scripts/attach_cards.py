#!/usr/bin/env python3
"""Set image/image_caption/image_bubble on news.jsonl items whose card image exists (per cards/manifest.jsonl)."""
import json, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man={}
mp=os.path.join(R,"cards","manifest.jsonl")
if os.path.exists(mp):
  for l in open(mp,encoding="utf-8"):
    if l.strip():
      m=json.loads(l); man[m["id"]]=m
p=os.path.join(R,"news.jsonl"); out=[]; n=0
for l in open(p,encoding="utf-8"):
  if not l.strip(): continue
  i=json.loads(l); m=man.get(i["id"],{}); f=m.get("file") or i.get("image")
  if f and os.path.exists(os.path.join(R,f)):
    i["image"]=f; n+=1
    if m.get("headline"):
      i["image_caption"]=m["headline"]; i["image_bubble"]=m["bubble"]
  else:
    for k in ("image","image_caption","image_bubble"): i.pop(k,None)
  out.append(json.dumps(i,ensure_ascii=False))
open(p,"w",encoding="utf-8").write("\n".join(out)+"\n")
print(f"{n} items have card images")
