/* Progressive enhancement. All stories and navigation work without JavaScript. */
(() => {
  const byId = (id) => document.getElementById(id);
  const toggle = byId("theme-toggle");
  const syncTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    const dark = theme === "dark";
    toggle.setAttribute("aria-pressed", String(dark));
    toggle.title = dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro";
    document.querySelector('meta[name="theme-color"]').content = dark
      ? "#101311"
      : "#f5f3ed";
  };
  if (toggle) {
    toggle.hidden = false;
    syncTheme(document.documentElement.dataset.theme);
    toggle.addEventListener("click", () => {
      const theme =
        document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      syncTheme(theme);
      try {
        localStorage.setItem("iaenlapyme-theme", theme);
      } catch (error) {
        /* Choice still works in memory. */
      }
    });
    window.addEventListener("storage", (event) => {
      if (event.key === "iaenlapyme-theme")
        syncTheme(event.newValue === "light" ? "light" : "dark");
    });
  }
  const search = byId("q");
  if (search) {
    const ids = ["q", "giro", "tarea", "herr", "pais"];
    const cards = [...document.querySelectorAll("#list .card")];
    const reset = byId("reset-filters");
    const menu = document.querySelector(".category-menu");
    const categoryButtons = [...menu.querySelectorAll("button")];
    let category = "";
    menu.hidden = false;
    const normalize = (value) =>
      value
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
    const filter = () => {
      const query = normalize(search.value);
      let count = 0;
      cards.forEach((card) => {
        const data = card.dataset;
        const matches =
          (!query || normalize(data.txt).includes(query)) &&
          (!category || data.categories.split("|").includes(category)) &&
          ["giro", "tarea", "pais"].every(
            (id) => !byId(id).value || data[id] === byId(id).value,
          ) &&
          (!byId("herr").value ||
            data.herr.split("|").includes(byId("herr").value));
        card.hidden = !matches;
        if (matches) count++;
      });
      byId("n").textContent = count + (count === 1 ? " caso" : " casos");
      byId("empty-state").hidden = count !== 0;
      reset.hidden = !category && !ids.some((id) => byId(id).value);
      categoryButtons.forEach((button) =>
        button.setAttribute(
          "aria-pressed",
          String(button.dataset.category === category),
        ),
      );
    };
    categoryButtons.forEach((button) =>
      button.addEventListener("click", () => {
        category = button.dataset.category;
        filter();
      }),
    );
    const clear = () => {
      category = "";
      ids.forEach((id) => {
        byId(id).value = "";
      });
      filter();
      search.focus({ preventScroll: true });
    };
    ids.forEach((id) => byId(id).addEventListener("input", filter));
    reset.addEventListener("click", clear);
    byId("empty-reset").addEventListener("click", clear);
    document
      .querySelector(".filter-panel")
      .addEventListener("submit", (event) => event.preventDefault());
    filter();
  }

  // Animate decorative layers only, with one frame per scroll and no layout reads
  // in the scroll handler. Small screens and reduced-motion users get a still image.
  const art = document.querySelector(".hero-art");
  if (!art) return;
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  const desktop = matchMedia("(min-width: 761px)");
  const layers = [...art.querySelectorAll("[data-parallax]")];
  let visible = true;
  let frame = 0;
  const draw = () => {
    frame = 0;
    if (motion.matches || !desktop.matches || !visible) return;
    const offset = Math.min(window.scrollY, 800);
    layers.forEach((layer) => {
      layer.style.transform = `translate3d(0, ${offset * Number(layer.dataset.parallax)}px, 0)`;
    });
  };
  const schedule = () => {
    if (!motion.matches && desktop.matches && visible && !frame)
      frame = requestAnimationFrame(draw);
  };
  const configure = () => {
    layers.forEach((layer) => {
      layer.style.transform = "";
    });
    schedule();
  };
  if ("IntersectionObserver" in window) {
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      schedule();
    }).observe(art);
  }
  window.addEventListener("scroll", schedule, { passive: true });
  motion.addEventListener("change", configure);
  desktop.addEventListener("change", configure);
  configure();
})();
