import json, os, subprocess, sys, threading, functools, http.server, socketserver, pytest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site"); PREFIX = "/iaenlapyme"
BASE = "https://allancrazyprogrammer.github.io/iaenlapyme"

@pytest.fixture(scope="session")
def build():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "gen", "build.py")], capture_output=True, text=True)
    return r

@pytest.fixture(scope="session")
def casos():
    d = json.load(open(os.path.join(ROOT, "data", "casos.json")))
    b = os.path.join(ROOT, "data", "borradores.json")
    return d + (json.load(open(b)) if os.path.exists(b) else [])

@pytest.fixture(scope="session")
def publicados(casos): return [c for c in casos if not c.get("borrador")]

@pytest.fixture(scope="session")
def server(build, tmp_path_factory):
    # serve site under /iaenlapyme/ like GitHub Pages
    root = tmp_path_factory.mktemp("srv"); os.symlink(SITE, root / "iaenlapyme")
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    h.log_message = lambda *a: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h); threading.Thread(target=s.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{s.server_address[1]}{PREFIX}"
    s.shutdown()

@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); yield b; b.close()
