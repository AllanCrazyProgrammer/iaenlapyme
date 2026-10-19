import json,html,os,shutil
from pathlib import Path
B="https://allancrazyprogrammer.github.io/iaenlapyme"; P="/iaenlapyme"; R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S=os.environ.get("OUT",R+"/site")
casos=[c for c in json.load(open(R+"/data/casos.json")) if not c.get("borrador")]
e=html.escape
VOTE_API="https://abacus.jasoncameron.dev"; VOTE_NS="allancrazyprogrammer-iaenlapyme"
def qh(c):
    q=c.get('que_hace') or []
    return ('<dt>Qué hace la IA</dt><dd><ul class="qh">'+''.join(f'<li>{e(x)}</li>' for x in q)+'</ul></dd>') if q else ''
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
CSS=Path(R+"/gen/style.css").read_text(encoding="utf-8")
NL="""<section class="box nl" id="boletin" aria-labelledby="newsletter-title"><div class="nl-intro"><span class="eyebrow">EN TU BANDEJA DE ENTRADA</span><h2 id="newsletter-title">Ideas que merecen<br>abrirse.</h2><p>El boletín semanal. 5 casos reales de IA en negocios como el tuyo, cada semana. Gratis.</p><span class="newsletter-arrow" aria-hidden="true">↗</span></div><div class="nl-form"><span class="eyebrow">UNA DOSIS SEMANAL DE INSPIRACIÓN</span>
<script async data-uid="5e51021646" src="https://ia-en-la-pyme.kit.com/5e51021646/index.js"></script>
<p class="nl-fb" hidden><a class="btn" href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener">Suscríbete gratis ↗</a></p>
<noscript><p><a class="btn" href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener">Suscríbete gratis ↗</a></p></noscript>
<p class="nl-help"><a href="https://ia-en-la-pyme.kit.com/5e51021646" target="_blank" rel="noopener">¿No ves el formulario? Suscríbete aquí ↗</a></p></div>
<script>setTimeout(()=>{if(!document.querySelector('.nl .formkit-form input[type=email]'))document.querySelectorAll('.nl-fb').forEach(p=>p.hidden=false)},5000)</script></section>"""
ARROW='<svg class="icon-arrow" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(t,desc,body,path,extra=""):
    url=B+path; body=body.replace("{P}",P)
    nav=lambda href,label: f'<a href="{P}{href}"'+(' aria-current="page"' if path==href else '')+f'>{label}</a>'
    page_class="home" if path=="/" else "detail" if path.startswith("/casos/") else "interior"
    result=f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f5f3ed"><link rel="stylesheet" href="{P}/style.css"><script defer src="{P}/site.js"></script>{extra}</head><body class="{page_class}"><a class="skip-link" href="#main">Saltar al contenido</a><header class="site-header"><div class="nav-wrap"><a class="logo" href="{P}/"><span class="brand-icon" aria-hidden="true">i<span>·</span></span><span>IA en la <strong>PyME</strong><small aria-hidden="true">INTELIGENCIA ARTIFICIAL, NEGOCIOS REALES</small></span></a><nav aria-label="Navegación principal">{nav('/','Explora los casos')}{nav('/manda-tu-caso/','Manda tu caso')}{nav('/patrocina/','Patrocina')}</nav><a class="nav-newsletter" href="{P}/#boletin">El boletín <span aria-hidden="true">↗</span></a></div></header>
<main id="main" tabindex="-1">{body}</main><footer class="site-footer"><a class="footer-brand" href="{P}/">IA en la PyME<span aria-hidden="true">↗</span></a><p>Casos reales, con su fuente.<br>Si algo está mal, avísanos.</p><a href="{P}/manda-tu-caso/">Construyamos el directorio juntos ↗</a></footer></body></html>"""
    return result.replace("↗",ARROW)
def card(c):
    index=casos.index(c)+1
    return f"""<a class="card" href="{P}/casos/{c['id']}/" data-giro="{e(c['giro'])}" data-tarea="{e(c['tarea'])}" data-pais="{e(c['pais'])}" data-herr="{e('|'.join(c['herramientas']))}" data-txt="{e((c['nombre']+' '+c['giro']+' '+c['tarea']+' '+' '.join(c['herramientas'])+' '+c['resultado']).lower())}">
<div class="card-top"><span class="case-index">CASO / {index:02d}</span><span class="country">{e(c['pais'])}</span></div><p class="card-sector">{e(c['giro'])}</p><h3>{e(c['nombre'])}</h3><div class="card-tags"><span class="tag">{e(c['tarea'])}</span><span class="tag ev-{c['evidencia']}"><span aria-hidden="true">●</span> evidencia {c['evidencia']}</span></div>
<p class="card-result">{e(c['resultado'] or 'La fuente no da cifras.')}</p><div class="card-bottom"><span>Explorar el caso</span><span class="card-arrow" aria-hidden="true">↗</span></div></a>"""
shutil.rmtree(S,ignore_errors=True); os.makedirs(S)
open(S+"/style.css","w").write(CSS)
shutil.copyfile(R+"/gen/site.js",S+"/site.js")
def opts(k,lab,vals): return f'<select id="{k}" aria-label="{lab}"><option value="">{lab}: todos</option>'+"".join(f'<option>{e(v)}</option>' for v in sorted(set(vals)))+"</select>"
herrs=[h for c in casos for h in c["herramientas"]]
body=f"""<section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span> EL DIRECTORIO DE IA PARA NEGOCIOS REALES</p><h1 id="hero-title">Casos reales de IA en <em>pequeños negocios.</em></h1><p class="hero-description">{len(casos)} historias de negocios de México, LatAm y España: qué hicieron, con qué herramienta y qué resultado dicen haber tenido, cada una con su fuente.</p><a class="btn primary" href="#directorio">Encuentra tu próxima idea <span aria-hidden="true">↓</span></a><p class="hero-footnote">Menos ruido. Más ejemplos que puedes explorar.</p></div><div class="hero-art" aria-hidden="true"><div class="art-grid"></div><div class="orbit orbit-one" data-parallax="0.035"></div><div class="orbit orbit-two" data-parallax="-0.025"></div><span class="art-label">CONEXIONES QUE TRANSFORMAN</span><div class="core" data-parallax="0.018"><span>IA</span><small>EN ACCIÓN</small></div><div class="node node-one" data-parallax="-0.025"><span class="node-symbol">↗</span><span>Ventas<small>NUEVAS POSIBILIDADES</small></span></div><div class="node node-two" data-parallax="0.025"><span class="node-symbol">≋</span><span>Inventario<small>EL DÍA A DÍA, MÁS SIMPLE</small></span></div><div class="node node-three" data-parallax="-0.018"><span class="node-symbol">✳</span><span>Atención<small>CONVERSACIONES CON VALOR</small></span></div><span class="art-caption">La tecnología cambia.<br>Las ideas se comparten.</span><span class="art-plus">+</span></div></section>
<div class="manifesto"><span>LA IA, A PIE DE NEGOCIO</span><p>De la idea a la práctica.<br><strong>Conoce quién ya dio el paso.</strong></p><a href="{P}/manda-tu-caso/">¿Tienes una historia? Compártela ↗</a></div>
<section class="directory" id="directorio" aria-labelledby="directory-title"><div class="section-heading"><div><p class="eyebrow">EXPLORA EL DIRECTORIO</p><h2 id="directory-title">Un caso puede ser<br>tu punto de partida<span>.</span></h2></div><p>Busca por lo que necesitas resolver.<br>Cada historia incluye su fuente y nivel de evidencia.</p></div>
<form class="filter-panel" role="search" aria-label="Buscar y filtrar casos"><div class="search-field"><label for="q">¿Qué quieres mejorar en tu negocio?</label><input id="q" type="search" placeholder="Busca: WhatsApp, inventario, facturas…" aria-controls="list"></div><div class="f">{opts('giro','Giro',[c['giro'] for c in casos])}{opts('tarea','Tarea',[c['tarea'] for c in casos])}{opts('herr','Herramienta',herrs)}{opts('pais','País',[c['pais'] for c in casos])}</div></form>
<div class="results-bar"><p id="n" role="status" aria-live="polite" aria-atomic="true">{len(casos)} casos</p><button type="button" id="reset-filters" hidden>Limpiar filtros <span aria-hidden="true">×</span></button><span class="results-note">HISTORIAS CON FUENTE, SIEMPRE</span></div><div class="grid" id="list">{''.join(card(c) for c in casos)}</div><div class="empty-state" id="empty-state" hidden><span aria-hidden="true">⌕</span><h3>No encontramos casos con esos filtros.</h3><p>Prueba otra palabra o amplía la búsqueda.</p><button type="button" id="empty-reset">Ver todos los casos ↗</button></div></section>{NL}"""
open(S+"/index.html","w").write(page("IA en la PyME: casos reales de inteligencia artificial en pequeños negocios","Directorio de casos reales de IA en PyMEs de México y LatAm: WhatsApp, ventas, inventario, contabilidad. Cada caso con su fuente.",body,"/"))
for c in casos:
    t=title(c); d=f"{c['nombre']} ({c['pais']}): {c['resultado'] or 'caso de IA en '+c['tarea'].lower()}"[:155]
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":t,"inLanguage":"es","citation":c["fuente"]},ensure_ascii=False)
    b=f"""<a class="back-link" href="{P}/#directorio">← Todos los casos</a><div class="article-heading"><p class="eyebrow">HISTORIAS DE IA EN LA PRÁCTICA / {e(c['pais'])}</p><h1>{e(t)}</h1><p class="tag ev-{c['evidencia']}">Nivel de evidencia: {c['evidencia']}</p></div>
<div class="box"><dl><dt>Negocio</dt><dd>{e(c['nombre'])}</dd><dt>País</dt><dd>{e(c['pais'])}</dd><dt>Giro</dt><dd>{e(c['giro'])}</dd><dt>Tarea</dt><dd>{e(c['tarea'])}</dd>
<dt>Herramientas</dt><dd>{e(', '.join(c['herramientas']))}</dd><dt>Costo aproximado</dt><dd>{e(c['costo'] or 'No lo dice la fuente')}</dd>
{qh(c)}<dt>Resultado (tal como lo dice la fuente)</dt><dd>{e(c['resultado'] or 'La fuente no da cifras.')}</dd><dt>Fuente</dt><dd><a href="{e(c['fuente'])}" rel="nofollow noopener" target="_blank">{e(c['fuente'])}</a></dd>
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
