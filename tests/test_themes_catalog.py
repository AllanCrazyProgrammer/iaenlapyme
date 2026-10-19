"""Theme and catalog interactions. External calls are blocked in every test."""
import pytest
from conftest import PREFIX


@pytest.fixture
def catalog_page(browser, server):
    context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(server.split(PREFIX)[0]) else r.abort())
    page = context.new_page()
    yield page
    context.close()


def test_dark_default_even_with_light_os(catalog_page, server):
    p = catalog_page
    p.emulate_media(color_scheme="light", reduced_motion="reduce")
    p.goto(server + "/")
    assert p.locator("html").get_attribute("data-theme") == "dark"
    assert p.locator("#theme-toggle").get_attribute("aria-pressed") == "true"
    assert p.locator("body").evaluate("e => getComputedStyle(e).backgroundColor") == "rgb(16, 19, 17)"


def test_theme_persists_across_pages_reload_and_tabs(catalog_page, server):
    p = catalog_page
    p.goto(server + "/")
    p.click("#theme-toggle")
    assert p.locator("html").get_attribute("data-theme") == "light"
    assert p.locator("#theme-toggle").get_attribute("aria-pressed") == "false"
    assert p.evaluate("localStorage.getItem('iaenlapyme-theme')") == "light"
    p.goto(server + "/casos/rey-pez/")
    assert p.locator("html").get_attribute("data-theme") == "light"
    p.reload()
    assert p.locator("html").get_attribute("data-theme") == "light"
    other = p.context.new_page()
    other.goto(server + "/patrocina/")
    other.click("#theme-toggle")
    p.wait_for_function("document.documentElement.dataset.theme === 'dark'")
    assert p.locator("#theme-toggle").get_attribute("aria-pressed") == "true"
    assert p.locator('meta[name="theme-color"]').get_attribute("content") == "#101311"


def test_saved_theme_applied_before_stylesheet(catalog_page, server):
    p = catalog_page
    p.add_init_script("localStorage.setItem('iaenlapyme-theme','light')")
    observed = []
    def css_request(route):
        observed.append(p.evaluate("document.documentElement.dataset.theme"))
        route.continue_()
    p.route("**/style.css", css_request)
    p.goto(server + "/")
    assert observed == ["light"]
    assert p.locator("body").evaluate("e => getComputedStyle(e).backgroundColor") == "rgb(245, 243, 237)"


def test_theme_with_unavailable_storage(catalog_page, server):
    p = catalog_page
    p.add_init_script("Object.defineProperty(Storage.prototype,'getItem',{value(){throw new Error('blocked')}});Object.defineProperty(Storage.prototype,'setItem',{value(){throw new Error('blocked')}})")
    errors = []
    p.on("pageerror", lambda error: errors.append(str(error)))
    p.goto(server + "/")
    assert p.locator("html").get_attribute("data-theme") == "dark"
    p.locator("#theme-toggle").focus()
    p.keyboard.press("Space")
    assert p.locator("html").get_attribute("data-theme") == "light"
    p.fill("#q", "Rey Pez")
    assert p.locator(".card:visible").count() == 1
    assert not errors


def test_categories_filters_and_reset(catalog_page, server, publicados):
    p = catalog_page
    p.goto(server + "/")
    menu = p.locator(".category-menu")
    expected = {"atencion": "Prixz", "ventas": "Novabori", "pedidos": "Mr. Food", "finanzas": "Tamey", "operacion": "Rey Pez"}
    for category, business in expected.items():
        menu.locator(f'[data-category="{category}"]').click()
        assert p.locator(".card:visible").filter(has_text=business).count() == 1
        assert p.locator(f'.card:visible:not([data-categories*="{category}"])').count() == 0
        assert menu.locator('[aria-pressed="true"]').count() == 1
    # Multi-task cases belong to every relevant category, rather than being
    # lost when a reader chooses a different task from their headline.
    for category in ["pedidos", "finanzas", "operacion"]:
        menu.locator(f'[data-category="{category}"]').click()
        assert p.locator(".card:visible").filter(has_text="Rey Pez").count() == 1
    p.fill("#q", "Rey Pez")
    p.select_option("#pais", "México")
    assert p.locator(".card:visible").count() == 1
    p.select_option("#pais", "Argentina")
    assert p.locator("#empty-state").is_visible()
    p.click("#empty-reset")
    assert p.locator(".card:visible").count() == len(publicados)
    assert menu.locator('[data-category=""]').get_attribute("aria-pressed") == "true"
    assert p.locator("#q").evaluate("e => e === document.activeElement")


@pytest.mark.parametrize("theme", ["dark", "light"])
@pytest.mark.parametrize("width", [320, 375, 390, 540, 768, 1440])
def test_poster_columns_and_legibility(catalog_page, server, theme, width):
    p = catalog_page
    p.set_viewport_size({"width": width, "height": 900})
    p.goto(server + "/")
    if theme == "light":
        p.click("#theme-toggle")
    assert p.evaluate("document.documentElement.scrollWidth") <= width
    columns = p.locator(".grid").evaluate("e => getComputedStyle(e).gridTemplateColumns.split(' ').length")
    assert columns == (2 if width <= 760 else 3 if width <= 1200 else 4)
    assert p.locator(".card h3").first.evaluate("e => parseFloat(getComputedStyle(e).fontSize)") >= 20
    for card in p.locator(".card").all():
        assert card.evaluate("e => e.scrollWidth <= e.clientWidth")
        assert card.locator("img").get_attribute("src").startswith(PREFIX + "/covers/")
        assert card.locator("img").get_attribute("alt") == ""
        assert card.locator(".card-bottom").inner_text().strip() == "Ver detalles"


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_all_pages_both_palettes(catalog_page, server, theme):
    p = catalog_page
    p.goto(server + "/")
    if theme == "light":
        p.click("#theme-toggle")
    for path in ["/", "/casos/rey-pez/", "/manda-tu-caso/", "/patrocina/", "/404.html"]:
        p.goto(server + path)
        assert p.locator("html").get_attribute("data-theme") == theme
        assert p.evaluate("document.documentElement.scrollWidth") <= 390
        assert p.locator("h1").is_visible()
