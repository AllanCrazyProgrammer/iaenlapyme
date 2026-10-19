# Directorio visual y temas claro/oscuro

El directorio conserva sus 23 casos y toda su información. Las tarjetas usan portadas vectoriales originales por categoría, degradado inferior, título destacado, etiquetas y enlace «Ver detalles». Los resultados completos siguen visibles, sin recortes ni cifras nuevas. No se añadieron noticias ficticias, imágenes de películas, vencimientos ni estados de pendiente.

## Navegación y diseño adaptable

El enlace «Explora los casos» lleva directamente al directorio. El menú de categorías utiliza botones nativos con `aria-pressed` y se puede desplazar horizontalmente en móvil. Son filtros combinables con búsqueda, giro, tarea, herramienta y país; «Limpiar filtros» y el estado vacío restablecen también la categoría.

Las categorías se derivan de las tareas reales. Un caso puede aparecer en varias: por ejemplo, Rey Pez figura en pedidos, contabilidad e inventario y operación. La portada corresponde a su primera categoría; las etiquetas conservan la tarea original completa.

La cuadrícula muestra dos columnas hasta 760 px, tres hasta 1200 px y cuatro en pantallas mayores. Los títulos miden al menos 20 px en los tamaños verificados; los resultados, 13 px. Las tarjetas crecen para mostrar el texto completo. Las portadas SVG son decorativas (`alt=""`), cargan de forma diferida y no dependen de servicios externos. Se añadieron en `gen/covers/` y se copian durante el build.

## Tema

La primera visita usa el modo oscuro, incluso cuando el sistema operativo prefiere el modo claro. El botón circular de la cabecera tiene nombre accesible «Modo oscuro», estado `aria-pressed`, foco visible y acceso por teclado.

La elección se guarda en `localStorage` con la clave `iaenlapyme-theme`. Un script pequeño en el encabezado aplica la preferencia antes de cargar la hoja de estilos para evitar un destello claro. La elección persiste entre páginas y recargas y se sincroniza entre pestañas. Si el almacenamiento está bloqueado, el selector sigue funcionando durante la visita.

`gen/catalog.css` amplía el sistema editorial previo. El generador concatena ambas hojas en un solo `style.css`. Se mantienen el parallax decorativo, su pausa fuera de pantalla y su desactivación en móvil o con movimiento reducido. Los efectos de las portadas también respetan `prefers-reduced-motion`. El formulario Tally conserva una superficie clara para su contenido de terceros.

## Verificación en nube

- Build correcto con el generador Python existente y sin nuevas dependencias de ejecución.
- 57 pruebas: las 38 anteriores más 19 de categorías, combinación de filtros, dos columnas, legibilidad, ambas paletas, tema inicial, persistencia entre páginas/recargas/pestañas, aplicación antes del CSS y almacenamiento bloqueado.
- Se verificaron anchos de 320, 375, 390, 540, 768 y 1440 px en ambas paletas, sin desbordes de documento ni de tarjetas.
- Auditoría axe-core con reglas WCAG 2 A/AA, WCAG 2.1 A/AA y buenas prácticas: sin infracciones automáticas en inicio, Rey Pez, envío, patrocinio y error, en ambas paletas a 390 y 1440 px (20 combinaciones). Es una comprobación automática, no una certificación completa con lectores de pantalla.
- Capturas de ambas paletas en `docs/screenshots/poster-*.png`; informe de auditoría en `docs/audits/catalog-themes.json`.

El proxy del entorno bloquea la descarga de la captura de referencia de Library y la apertura directa de GitHub Pages, Kit y Tally. Se utilizó la descripción visual proporcionada de la referencia. Las comprobaciones de Kit y votos usan simulación y respaldo; no se envían formularios ni votos reales. La revisión visual corresponde al build servido en la nube con Chromium. La publicación utiliza el workflow existente de GitHub Pages, sin modificar cuentas, permisos, dominios ni servicios de pago.
