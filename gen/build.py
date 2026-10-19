import json,html,os,re,unicodedata,shutil
import os
B="https://allancrazyprogrammer.github.io/iaenlapyme"; P="/iaenlapyme"; R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S=os.environ.get("OUT",R+"/site")
casos=[c for c in json.load(open(R+"/data/casos.json")) if not c.get("borrador")]
e=html.escape
VOTE_API="https://abacus.jasoncameron.dev"; VOTE_NS="allancrazyprogrammer-iaenlapyme"
def vote(c):
    # Contador público sin cuenta (Abacus). Si el servicio falla, el bloque se queda oculto.
    return ('<div class="box vote" id="vote" hidden data-api="'+VOTE_API+'" data-ns="'+VOTE_NS+'" data-key="caso-'+e(c['id'])+'">'
    '<button type="button" id="vbtn">👍 Me sirvió</button> <span id="vn" aria-live="polite"></span></div>'
    """<script>(()=>{const v=document.getElementById('vote'),b=document.getElementById('vbtn'),n=document.getElementById('vn'),d=v.dataset,u=a=>d.api+'/'+a+'/'+d.ns+'/'+d.key,lk='voto:'+d.key;
let st=()=>{try{return localStorage.getItem(lk)}catch(x){return null}},sv=()=>{try{localStorage.setItem(lk,'1')}catch(x){}};
const go=(a)=>{const c=new AbortController(),t=setTimeout(()=>c.abort(),6000);return fetch(u(a),{signal:c.signal}).then(r=>{clearTimeout(t);if(a=='get'&&r.status==404)return {value:0};if(!r.ok)throw r.status;return r.json()}).then(j=>{if(typeof j.value!='number')throw 'x';return j.value})};
const show=x=>{n.textContent=x==0?'¿Te sirvió? Sé la primera persona en decirlo':x==1?'A 1 persona le sirvió':'A '+x+' personas les sirvió'};const done=()=>{b.disabled=true;b.textContent='✓ Te sirvió'};
go('get').then(x=>{show(x);if(st())done();v.hidden=false}).catch(()=>{});
b.addEventListener('click',()=>{if(st())return;b.disabled=true;go('hit').then(x=>{sv();show(x);done()}).catch(()=>{b.disabled=false;n.textContent='No se pudo registrar tu voto. Intenta más tarde.'})});})()</script>""")
def art(g):
    g=g.lower(); return ("una "+g) if g.split()[0].endswith(("a","ería","ción")) else ("un negocio de "+g)
def title(c): return f"Cómo {art(c['giro'])} en {c['pais']} usa IA para {c['tarea'][0].lower()+c['tarea'][1:]}"
CSS="""*{box-sizing:border-box}[hidden]{display:none!important}body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#1d2330;background:#f7f8fa;line-height:1.55}
a{color:#0b6e4f}header{background:#0b6e4f;color:#fff;padding:14px 16px}header a{color:#fff;text-decoration:none;margin-right:14px;font-size:.95rem}
header .logo{font-weight:800;font-size:1.15rem}main{max-width:960px;margin:auto;padding:16px}
.hero h1{font-size:1.7rem;margin:.4em 0}.f{display:grid;gap:8px;grid-template-columns:1fr 1fr}.f input{grid-column:1/-1}
input,select,textarea,button{font:inherit;padding:10px;border:1px solid #cdd3dc;border-radius:8px;width:100%}button{background:#0b6e4f;color:#fff;border:0;cursor:pointer}
.grid{display:grid;gap:12px;margin-top:16px}.card{background:#fff;border-radius:12px;padding:14px;box-shadow:0 1px 3px #0001;text-decoration:none;color:inherit;display:block}
.card h3{margin:.2em 0 .4em;font-size:1.05rem}.tag{display:inline-block;font-size:.75rem;background:#e6f2ee;color:#0b6e4f;border-radius:99px;padding:2px 8px;margin:2px}
.ev-alto{background:#d1f5d3}.ev-bajo{background:#fdeccc;color:#8a5a00}.box{background:#fff;border-radius:12px;padding:16px;margin:18px 0;box-shadow:0 1px 3px #0001}
.nl{background:#102a43;color:#fff}.nl form{display:flex;gap:8px}.nl button{width:auto;background:#f0b429;color:#102a43;font-weight:700}
footer{text-align:center;font-size:.85rem;color:#667;padding:24px}dl dt{font-weight:700;margin-top:10px}dl dd{margin:0;overflow-wrap:anywhere}
.vote{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.vote button{width:auto;padding:10px 16px;font-weight:700}.vote button:disabled{background:#8fb8aa;cursor:default}
.nl .btn{display:inline-block;background:#f0b429;color:#102a43;font-weight:700;padding:12px 20px;border-radius:8px;text-decoration:none}
.nl .formkit-form .formkit-background{display:none!important}.nl .formkit-form .formkit-column{padding:16px!important}
.nl .formkit-form .formkit-header{margin:0 0 8px!important}.nl .formkit-form .formkit-header h2{font-size:1.2rem!important;margin:0!important;line-height:1.3}
.nl .formkit-form .formkit-input{color:#1d2330!important;padding:10px 12px!important;border:1px solid #cdd3dc!important;border-radius:8px!important}.nl .formkit-form .formkit-submit{background-color:#f0b429!important;color:#102a43!important;border-radius:8px!important}
@media(min-width:700px){.f{grid-template-columns:2fr 1fr 1fr 1fr 1fr}.f input{grid-column:auto}.grid{grid-template-columns:1fr 1fr}}"""
NL="""<section class="box nl"><h2>El boletín semanal</h2><p>5 casos reales de IA en negocios como el tuyo, cada semana. Gratis.</p>
<script async data-uid="5e51021646" src="https://ia-en-la-pyme.kit.com/5e51021646/index.js"></script>
<p class="nl-fb" hidden><a class="btn" href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener">Suscríbete gratis</a></p>
<noscript><p><a class="btn" href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener">Suscríbete gratis</a></p></noscript>
<p><a href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener" style="color:#f0b429">¿No ves el formulario? Suscríbete aquí</a></p>
<script>setTimeout(()=>{if(!document.querySelector('.nl .formkit-form input[type=email]'))document.querySelectorAll('.nl-fb').forEach(p=>p.hidden=false)},5000)</script></section>"""
def page(t,desc,body,path,extra=""):
    url=B+path; body=body.replace("{P}",P)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{P}/style.css">{extra}</head><body><header><a class="logo" href="{P}/">IA en la PyME</a><a href="{P}/manda-tu-caso/">Manda tu caso</a><a href="{P}/patrocina/">Patrocina</a></header>
<main>{body}</main><footer>IA en la PyME · Casos reales, con su fuente. Si algo está mal, avísanos.</footer></body></html>"""
def card(c): 
    return f"""<a class="card" href="{P}/casos/{c['id']}/" data-giro="{e(c['giro'])}" data-tarea="{e(c['tarea'])}" data-pais="{e(c['pais'])}" data-herr="{e('|'.join(c['herramientas']))}" data-txt="{e((c['nombre']+' '+c['giro']+' '+c['tarea']+' '+' '.join(c['herramientas'])+' '+c['resultado']).lower())}">
<h3>{e(c['nombre'])}</h3><span class="tag">{e(c['pais'])}</span><span class="tag">{e(c['tarea'])}</span><span class="tag ev-{c['evidencia']}">evidencia {c['evidencia']}</span>
<p>{e(c['resultado'] or 'La fuente no da cifras.')}</p></a>"""
shutil.rmtree(S,ignore_errors=True); os.makedirs(S)
open(S+"/style.css","w").write(CSS)
def opts(k,lab,vals): return f'<select id="{k}" aria-label="{lab}"><option value="">{lab}: todos</option>'+"".join(f'<option>{e(v)}</option>' for v in sorted(set(vals)))+"</select>"
herrs=[h for c in casos for h in c["herramientas"]]
body=f"""<section class="hero"><h1>Casos reales de IA en pequeños negocios</h1><p>{len(casos)} historias de negocios de México, LatAm y España: qué hicieron, con qué herramienta y qué resultado dicen haber tenido, cada una con su fuente.</p></section>
<div class="f"><input id="q" type="search" placeholder="Busca: WhatsApp, inventario, facturas…" aria-label="Buscar">{opts('giro','Giro',[c['giro'] for c in casos])}{opts('tarea','Tarea',[c['tarea'] for c in casos])}{opts('herr','Herramienta',herrs)}{opts('pais','País',[c['pais'] for c in casos])}</div>
<p id="n"></p><div class="grid" id="list">{''.join(card(c) for c in casos)}</div>{NL}
<script>const $=i=>document.getElementById(i),f=()=>{{let q=$('q').value.toLowerCase(),n=0;document.querySelectorAll('.card').forEach(c=>{{let d=c.dataset,ok=(!q||d.txt.includes(q))&&(!$('giro').value||d.giro==$('giro').value)&&(!$('tarea').value||d.tarea==$('tarea').value)&&(!$('pais').value||d.pais==$('pais').value)&&(!$('herr').value||d.herr.split('|').includes($('herr').value));c.hidden=!ok;n+=ok}});$('n').textContent=n+' casos'}};['q','giro','tarea','herr','pais'].forEach(i=>$(i).addEventListener('input',f));f()</script>"""
open(S+"/index.html","w").write(page("IA en la PyME: casos reales de inteligencia artificial en pequeños negocios","Directorio de casos reales de IA en PyMEs de México y LatAm: WhatsApp, ventas, inventario, contabilidad. Cada caso con su fuente.",body,"/"))
for c in casos:
    t=title(c); d=f"{c['nombre']} ({c['pais']}): {c['resultado'] or 'caso de IA en '+c['tarea'].lower()}"[:155]
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"inLanguage":"es","citation":c["fuente"]},ensure_ascii=False)
    b=f"""<p><a href="{P}/">← Todos los casos</a></p><h1>{e(t)}</h1><p class="tag ev-{c['evidencia']}">Nivel de evidencia: {c['evidencia']}</p>
<div class="box"><dl><dt>Negocio</dt><dd>{e(c['nombre'])}</dd><dt>País</dt><dd>{e(c['pais'])}</dd><dt>Giro</dt><dd>{e(c['giro'])}</dd><dt>Tarea</dt><dd>{e(c['tarea'])}</dd>
<dt>Herramientas</dt><dd>{e(', '.join(c['herramientas']))}</dd><dt>Costo aproximado</dt><dd>{e(c['costo'] or 'No lo dice la fuente')}</dd>
<dt>Resultado (tal como lo dice la fuente)</dt><dd>{e(c['resultado'] or 'La fuente no da cifras.')}</dd><dt>Fuente</dt><dd><a href="{e(c['fuente'])}" rel="nofollow noopener" target="_blank">{e(c['fuente'])}</a></dd>
<dt>Fecha</dt><dd>{e(c['fecha'] or '—')}</dd><dt>Nota</dt><dd>{e(c.get('nota',''))}</dd></dl></div>{vote(c)}{NL}"""
    os.makedirs(f"{S}/casos/{c['id']}"); open(f"{S}/casos/{c['id']}/index.html","w").write(page(t+" | IA en la PyME",d,b,f"/casos/{c['id']}/",f'<script type="application/ld+json">{ld}</script>'))
os.makedirs(S+"/manda-tu-caso"); open(S+"/manda-tu-caso/index.html","w").write(page("Manda tu caso de IA | IA en la PyME","¿Usas IA en tu negocio? Cuéntanos y lo publicamos con tu permiso.","""<h1>Manda tu caso</h1><p>¿Usas IA en tu negocio? Cuéntanos qué hiciste y qué cambió. Lo revisamos antes de publicar.</p>
<div class="box"><iframe data-tally-src="https://tally.so/embed/1WPYyl?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="900" frameborder="0" marginheight="0" marginwidth="0" title="Manda tu caso"></iframe>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach(function(e){e.src=e.dataset.tallySrc})};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s)}</script>
<noscript><p><a href="https://tally.so/r/1WPYyl">Abrir el formulario</a></p></noscript></div>
<p>¿No ves el formulario? <a href="https://tally.so/r/1WPYyl" target="_blank" rel="noopener">Ábrelo aquí</a>.</p>""","/manda-tu-caso/"))
os.makedirs(S+"/patrocina"); open(S+"/patrocina/index.html","w").write(page("Patrocina | IA en la PyME","Llega a dueños de PyMEs hispanas interesados en IA.","""<h1>Patrocina IA en la PyME</h1><p>Nuestros lectores son dueños y encargados de pequeños negocios en México y LatAm que buscan usar IA de verdad.</p>
<div class="box"><h2>Patrocinio del boletín</h2><p>Un espacio destacado en el correo semanal, marcado como patrocinio.</p></div>
<div class="box"><h2>Ficha de herramienta o agencia</h2><p>Tu herramienta o agencia en el directorio, enlazada a los casos donde aparece y marcada como "patrocinado".</p></div>
<div class="box"><h2>Reglas</h2><p>El patrocinio nunca cambia el nivel de evidencia de un caso ni el texto de su resultado.</p></div><p>¿Te interesa? Escríbenos a través de <a href="https://tally.so/r/1WPYyl" target="_blank" rel="noopener">este formulario</a> (menciona "patrocinio").</p>""","/patrocina/"))
urls=["/","/manda-tu-caso/","/patrocina/"]+[f"/casos/{c['id']}/" for c in casos]
open(S+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{B}{u}</loc></url>" for u in urls)+"</urlset>")
open(S+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {B}/sitemap.xml\n")
open(S+"/404.html","w").write(page("No encontrado | IA en la PyME","","<h1>Página no encontrada</h1><p><a href='{P}/'>Volver al inicio</a></p>","/404.html"))
open(S+"/.nojekyll","w").write("")
print(len(casos),"pages"); [print(title(c)) for c in casos[:6]]
