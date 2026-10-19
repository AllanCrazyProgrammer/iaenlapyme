/* Progressive enhancement. All stories and navigation work without JavaScript. */
(() => {
  const byId = (id) => document.getElementById(id);
  const search = byId("q");
  if (search) {
    const ids = ["q", "giro", "tarea", "herr", "pais"];
    const cards = [...document.querySelectorAll("#list .card")];
    const reset = byId("reset-filters");
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
      reset.hidden = !ids.some((id) => byId(id).value);
    };
    const clear = () => {
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
