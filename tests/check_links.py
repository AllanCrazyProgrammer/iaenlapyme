"""Revisa las URLs de fuente. Reporta rotas, nunca falla (exit 0)."""
import json, os, urllib.request, concurrent.futures as cf
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cs=[c for c in json.load(open(R+"/data/casos.json")) if c.get("fuente")]
def chk(c):
    u=c["fuente"]
    for m in ("HEAD","GET"):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,method=m,headers={"User-Agent":"Mozilla/5.0 (iaenlapyme link checker)"}),timeout=20)
            return c["id"],u,r.status
        except urllib.error.HTTPError as e:
            if m=="GET": return c["id"],u,e.code
        except Exception as e:
            if m=="GET": return c["id"],u,type(e).__name__
res=list(cf.ThreadPoolExecutor(8).map(chk,cs))
bad=[r for r in res if r[2]!=200]
for r in res: print(("OK  " if r[2]==200 else "ROTA"),r[2],r[0],r[1])
print(f"\n{len(res)-len(bad)}/{len(res)} OK, {len(bad)} con problema")
s=os.environ.get("GITHUB_STEP_SUMMARY")
if s: open(s,"a").write("## Enlaces de fuente\n"+"\n".join(f"- {r[2]} `{r[0]}` {r[1]}" for r in bad)+f"\n\n{len(res)-len(bad)}/{len(res)} OK\n")
