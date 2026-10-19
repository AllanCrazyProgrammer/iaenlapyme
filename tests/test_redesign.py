"""Interaction and accessibility regressions for the editorial redesign.
External services are isolated: these tests never submit or vote on live systems.
"""
import pytest
from conftest import PREFIX


@pytest.fixture
def isolated_page(browser, server):
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(server.split(PREFIX)[0]) else r.abort())
    page = context.new_page()
    yield page
    context.close()


def test_combined_filters_accent_search_and_reset(isolated_page, server, publicados):
    p = isolated_page
    p.goto(server + "/")
    p.fill("#q", "atencion")
    p.select_option("#pais", "México")
    p.select_option("#tarea", "Atención por WhatsApp")
    p.select_option("#giro", "Cafetería y comida a domicilio")
    p.select_option("#herr", "Chatbot con IA para WhatsApp (GreenChimp)")
    assert p.locator(".card:visible").count() == 1
    assert "Zenda Café" in p.locator(".card:visible").inner_text()
    assert p.locator("#n").inner_text() == "1 caso"
    p.click("#reset-filters")
    assert p.locator(".card:visible").count() == len(publicados)
    assert p.locator("#q").evaluate("e => e === document.activeElement")
    assert p.locator("#reset-filters").is_hidden()
    p.fill("#q", "sin-resultados-xyz")
    assert p.locator("#empty-state").is_visible()
    p.click("#empty-reset")
    assert p.locator(".card:visible").count() == len(publicados)
    assert p.locator("#empty-state").is_hidden()


def test_search_enter_does_not_reload(isolated_page, server):
    p = isolated_page
    p.goto(server + "/")
    p.fill("#q", "whatsapp")
    p.evaluate("window.testMarker = true")
    p.press("#q", "Enter")
    assert p.evaluate("window.testMarker")
    assert p.input_value("#q") == "whatsapp"


def test_keyboard_skip_link_and_landmarks(isolated_page, server):
    p = isolated_page
    p.goto(server + "/")
    p.keyboard.press("Tab")
    assert p.locator(".skip-link").evaluate("e => e === document.activeElement")
    p.keyboard.press("Enter")
    assert p.locator("main").evaluate("e => e === document.activeElement")
    assert p.locator("h1").count() == 1
    assert p.locator('nav[aria-label]').count() == 1
    assert p.locator("#n").get_attribute("aria-live") == "polite"


def test_motion_preferences_and_decorative_parallax(isolated_page, server):
    p = isolated_page
    p.emulate_media(reduced_motion="no-preference")
    p.goto(server + "/")
    p.evaluate("document.documentElement.style.scrollBehavior='auto'; scrollTo(0,200)")
    p.wait_for_function("document.querySelector('.core').style.transform.includes('3.6px')")
    assert p.locator(".hero-art").get_attribute("aria-hidden") == "true"
    p.emulate_media(reduced_motion="reduce")
    p.wait_for_function("getComputedStyle(document.querySelector('.core')).transform === 'none'")
    assert p.locator(".hero-copy").evaluate("e => getComputedStyle(e).animationName") == "none"
    p.set_viewport_size({"width": 390, "height": 844})
    p.emulate_media(reduced_motion="no-preference")
    p.evaluate("scrollTo(0,100)")
    assert p.locator(".core").evaluate("e => getComputedStyle(e).transform") == "none"


@pytest.mark.parametrize("width", [320, 390, 768, 1024, 1440])
def test_responsive_all_pages(isolated_page, server, width):
    p = isolated_page
    p.set_viewport_size({"width": width, "height": 900})
    for path in ["/", "/casos/rey-pez/", "/manda-tu-caso/", "/patrocina/", "/404.html"]:
        p.goto(server + path)
        assert p.evaluate("document.documentElement.scrollWidth") <= width, (width, path)
        assert p.locator("h1").is_visible()
        assert p.locator("nav").is_visible()


def test_directory_without_javascript(browser, server, publicados):
    context = browser.new_context(java_script_enabled=False)
    context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(server.split(PREFIX)[0]) else r.abort())
    p = context.new_page()
    p.goto(server + "/")
    assert p.locator(".card:visible").count() == len(publicados)
    assert p.locator("#n").inner_text() == str(len(publicados)) + " casos"
    assert p.locator(".nl noscript a").is_visible()
    p.locator('.card[href$="/rey-pez/"]').click()
    assert "cuarto frío" in p.locator("main").inner_text()
    context.close()


def test_all_case_content_preserved(build, publicados):
    import html
    from pathlib import Path
    from conftest import SITE
    for case in publicados:
        output = (Path(SITE) / 'casos' / case['id'] / 'index.html').read_text(encoding='utf-8')
        for field in ['nombre', 'pais', 'giro', 'tarea', 'costo', 'resultado', 'fuente', 'fecha', 'nota']:
            if case.get(field):
                assert html.escape(case[field]) in output, (case['id'], field)
        for item in case.get('que_hace', []):
            assert html.escape(item) in output, case['id']
        assert html.escape(', '.join(case['herramientas'])) in output, case['id']
