#!/usr/bin/env python3
"""Rebuild README.md, weekly.md, monthly.md from news.jsonl. Ratings are never printed."""
import json, glob, os, datetime as dt
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ=dt.timezone(dt.timedelta(hours=7))
M={"Mon":"Moe the Coffee Robot ☕🤖","Tue":"Turbo the Llama 🦙","Wed":"Wally the Wombat 🐨","Thu":"Thunder the Hamster ⚡🐹","Fri":"Fry the Party Penguin 🐧🎉","Sat":"Sid the Surfing Sloth 🦥🏄","Sun":"Sunny the Cat 🐱☀️"}
items=[json.loads(l) for l in open(os.path.join(R,"news.jsonl"),encoding="utf-8") if l.strip()]
today=max((i["discovered_at"][:10] for i in items),default=dt.datetime.now(TZ).date().isoformat())
td=dt.date.fromisoformat(today)
srt=lambda xs:sorted(xs,key=lambda i:-i["rating"])
def lst(xs): return "\n".join(f"{n}. **[{i['title']}]({i['url']})** {i.get('quip','')}" for n,i in enumerate(xs,1))
def tldr(xs): return "📰 **TL;DR:** "+" · ".join(i["title"] for i in xs[:3])+" 🔥🤯"
def win(days,top):
  lo=td-dt.timedelta(days=days-1)
  return srt([i for i in items if lo<=dt.date.fromisoformat(i["published_at"][:10])<=td])[:top]
t=srt([i for i in items if i["discovered_at"][:10]==today])
day=td.strftime("%a"); mascot=M[day]
comic=sorted(glob.glob(os.path.join(R,"comics",f"{today}-*.jpg")))
out=[f"# 🤖 AI News Digest\n\nDaily AI news from [4PDA's AI forum](https://4pda.to/forum/index.php?showforum=1240), curated with r/LocalLLaMA energy 🦾. Updated every day at 9:17 AM (UTC+7).\n\n📅 **{today}** · Mascot of the day: **{mascot}**\n\nSee also: [🗓️ Top of the week](weekly.md) · [📆 Top of the month](monthly.md)\n"]
if comic: out.append(f"![Today's comic](comics/{os.path.basename(comic[-1])})\n")
out+= [tldr(t),"",lst(t),""]
open(os.path.join(R,"README.md"),"w",encoding="utf-8").write("\n".join(out))
for fn,days,top,h in [("weekly.md",7,10,"🗓️ Top of the week"),("monthly.md",30,20,"📆 Top of the month")]:
  x=win(days,top)
  open(os.path.join(R,fn),"w",encoding="utf-8").write(f"# {h}\n\nLast {days} days up to {today} (by publication date). [⬅️ Today](README.md)\n\n{tldr(x)}\n\n{lst(x)}\n")
