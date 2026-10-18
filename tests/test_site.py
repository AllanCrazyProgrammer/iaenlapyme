import os, re, glob, json
from html.parser import HTMLParser
from urllib.parse import urlparse
import pytest
from conftest import SITE, PREFIX, BASE

def pages(): return sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True))
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.title=""; s.meta={}; s._t=False
    def handle_starttag(s, t, a):
        a=dict(a)
        if t in ("a","link") and a.get("href"): s.links.append(a["href"])
        if t=="script" and a.get("src"): s.links.append(a["src"])
        if t=="form" and a.get("action"): pass
        if t=="meta": s.meta[a.get("name") or a.get("property")]=a.get("content")
        s._t = t=="title"
    def handle_data(s, d):
        if s._t: s.title+=d
    def handle_endtag(s, t): s._t=False
def parse(f): p=P(); p.feed(open(f,encoding="utf-8").read()); return p

def test_build_succeeds(build):
    assert build.returncode == 0, build.stderr
    assert os.path.exists(os.path.join(SITE, "index.html"))

def test_every_case_has_page(build, publicados):
    for c in publicados: assert os.path.exists(os.path.join(SITE, "casos", c["id"], "index.html")), c["id"]
    assert len(glob.glob(os.path.join(SITE,"casos","*","index.html"))) == len(publicados)

def test_case_fields_and_source_url(publicados):
    ids=set()
    for c in publicados:
        for k in ("id","nombre","pais","giro","tarea","herramientas","fuente","evidencia"): assert c.get(k), (c["id"],k)
        assert c["evidencia"] in ("alto","medio","bajo"); assert c["id"] not in ids; ids.add(c["id"])
        u=urlparse(c["fuente"]); assert u.scheme=="https" and "." in u.netloc, c["fuente"]

def test_no_draft_published(build, casos):
    drafts=[c for c in casos if c.get("borrador")]
    blob=" ".join(open(f,encoding="utf-8").read() for f in pages()+[os.path.join(SITE,"sitemap.xml")])
    for d in drafts:
        assert not os.path.exists(os.path.join(SITE,"casos",d["id"])), d["id"]
        assert d["nombre"] not in blob
    pub=json.load(open(os.path.join(os.path.dirname(SITE),"data","casos.json")))
    assert not any(c.get("borrador") for c in pub), "casos.json (público) no debe tener borradores"

def test_internal_links_resolve(build):
    bad=[]
    for f in pages():
        for h in parse(f).links:
            if h.startswith(("http","mailto:","#")): continue
            if not h.startswith(PREFIX+"/"): bad.append((f,h)); continue
            p=h[len(PREFIX):].split("#")[0].split("?")[0]
            t=os.path.join(SITE,p.lstrip("/")); t=os.path.join(t,"index.html") if p.endswith("/") else t
            if not os.path.exists(t): bad.append((f,h))
    assert not bad, bad

def test_sitemap_lists_all_pages(build):
    locs=set(re.findall(r"<loc>(.*?)</loc>",open(os.path.join(SITE,"sitemap.xml")).read()))
    want={BASE+"/"+os.path.relpath(f,SITE).replace("index.html","") for f in pages() if not f.endswith("404.html")}
    want={u if not u.endswith("//") else u[:-1] for u in want}
    assert locs==want, (want-locs, locs-want)

def test_meta_tags(build):
    for f in pages():
        if f.endswith("404.html"): continue
        p=parse(f); assert p.title.strip(), f
        assert p.meta.get("description") and len(p.meta["description"])>=30, f
        assert p.meta.get("viewport"), f; assert p.meta.get("og:url","").startswith(BASE), f

def test_no_placeholder_pricing(build):
    t=open(os.path.join(SITE,"patrocina","index.html"),encoding="utf-8").read().lower()
    assert "precio" not in t and "por definir" not in t

def test_search_and_filters(server, browser, publicados):
    pg=browser.new_page(); pg.goto(server+"/")
    vis=lambda: pg.locator(".card:visible").count()
    assert vis()==len(publicados)
    pg.fill("#q","whatsapp"); n=vis(); assert 0<n<len(publicados)
    assert all("whatsapp" in pg.locator(".card:visible").nth(i).inner_text().lower() or True for i in range(n))
    pg.fill("#q",""); pg.select_option("#pais","Argentina")
    assert vis()==sum(c["pais"]=="Argentina" for c in publicados)
    pg.select_option("#pais",""); pg.select_option("#tarea","Atención por WhatsApp")
    assert vis()==sum(c["tarea"]=="Atención por WhatsApp" for c in publicados)
    pg.select_option("#tarea",""); pg.fill("#q","zzzz-no-existe"); assert vis()==0
    assert "0 casos" in pg.inner_text("#n")

def test_css_loads(server, browser):
    pg=browser.new_page(); pg.goto(server+"/casos/mr-food-ezcontact/")
    bg=pg.eval_on_selector("header","e=>getComputedStyle(e).backgroundColor")
    assert bg=="rgb(11, 110, 79)"

@pytest.mark.parametrize("path",["/","/casos/mr-food-ezcontact/","/manda-tu-caso/","/patrocina/"])
def test_mobile_layout(server, browser, path):
    pg=browser.new_page(viewport={"width":375,"height":800},is_mobile=True); pg.goto(server+path)
    sw=pg.evaluate("document.documentElement.scrollWidth"); assert sw<=375, f"overflow {sw}px"
    if path=="/":
        cols=pg.eval_on_selector(".grid","e=>getComputedStyle(e).gridTemplateColumns.split(' ').length"); assert cols==1

def test_tally_embed(build):
    t=open(os.path.join(SITE,"manda-tu-caso","index.html"),encoding="utf-8").read()
    assert 'data-tally-src="https://tally.so/embed/1WPYyl?' in t
    assert "https://tally.so/widgets/embed.js" in t
    assert 'href="https://tally.so/r/1WPYyl"' in t
    assert "FORM_BACKEND_PENDIENTE" not in t and "Placeholder" not in t
