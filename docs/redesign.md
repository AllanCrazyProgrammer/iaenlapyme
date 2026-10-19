# Rediseño editorial de IA en la PyME

## Implementación

El sitio conserva su generador estático en Python y sus rutas de GitHub Pages bajo `/iaenlapyme/`. `data/casos.json` sigue siendo la fuente del contenido: no se modificaron casos, resultados, notas, cifras ni fuentes.

- `gen/build.py`: estructura semántica, portada, directorio, tarjetas y páginas interiores.
- `gen/style.css`: sistema visual editorial con papel claro, tinta, naranja y verde; tipografía del sistema y Georgia sin descargas de fuentes; distribución adaptable.
- `gen/site.js`: búsqueda sin distinguir acentos, filtros combinables, limpieza y estado vacío; parallax decorativo con `requestAnimationFrame`, eventos pasivos y pausa fuera de pantalla. Se desactiva en pantallas pequeñas y con `prefers-reduced-motion`.

La navegación, filtros originales, metadatos, sitemap, enlaces de fuentes, votos Abacus, formulario Kit y formulario Tally mantienen sus destinos e identificadores. El directorio y las páginas se pueden leer sin JavaScript. Se añadió un enlace para saltar al contenido, foco visible y anuncio del número de resultados.

## Construcción y pruebas

```sh
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python gen/build.py
.venv/bin/pytest -q tests
```

Si el entorno ya trae Chromium instalado, se puede indicar su ejecutable:

```sh
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium .venv/bin/pytest -q tests
```

Para una vista previa con el mismo prefijo que GitHub Pages:

```sh
mkdir -p /tmp/iaenlapyme-preview
ln -sfn "$PWD/site" /tmp/iaenlapyme-preview/iaenlapyme
.venv/bin/python -m http.server 8765 --directory /tmp/iaenlapyme-preview
```

Abrir `http://localhost:8765/iaenlapyme/`.

## Verificación en el entorno de nube

- Build correcto: 23 fichas de casos y páginas de inicio, envío, patrocinio y error.
- 38 pruebas: suite original, conservación de todo el contenido y regresiones de filtros combinados, búsqueda con acentos, teclado, ausencia de JavaScript, preferencia de movimiento y tamaños de 320, 390, 768, 1024 y 1440 px.
- Auditoría axe-core con reglas WCAG 2 A/AA, WCAG 2.1 A/AA y buenas prácticas: sin infracciones automáticas en inicio, Rey Pez, envío, patrocinio y error, a 390 y 1440 px. Esto no sustituye una auditoría manual completa con lectores de pantalla.
- Revisión visual con Chromium: portada, directorio y ficha de Rey Pez en escritorio y móvil. Capturas locales en `shots/` (carpeta excluida de Git, como antes).
- Sin nuevas dependencias de ejecución, imágenes pesadas, fuentes remotas ni bibliotecas de animación. Los activos propios de CSS y JavaScript suman aproximadamente 28 KB sin comprimir.

## Límites comprobados

El proxy de red del entorno responde HTTP 403 a los dominios de Kit y Tally. No fue posible inspeccionar sus formularios reales cargados desde estos proveedores. Se conservaron los embeds y enlaces originales; las pruebas de Kit usan el formulario simulado existente y verifican el respaldo cuando el servicio está bloqueado. Los votos se comprueban con la API simulada, incluido fallo del servicio y persistencia por navegador. No se enviaron formularios ni se registraron votos reales.

No se han vuelto a verificar las fuentes externas de los 23 casos; sus enlaces no cambiaron. Todos los enlaces internos se validan en la suite. La revisión de navegador se realizó con Chromium, sin Safari ni Firefox.

No se modificó el workflow de publicación. Este trabajo no implica una fusión a `main` ni un despliegue a producción.
