# Bitácora del agente

## Ciclo 1 — 2026-11-17
- Investigación: comisiones de plataformas (Gumroad 10%+0.50; Payhip 5%; Lemon Squeezy 5%+0.50) y categorías que más venden en Etsy en 2026 (planners, plantillas editables, wall art, hojas de cálculo).
- Decisión: empezar con un planner 2027, aprovechando su temporada alta.
- Creado `tools/planner2027.py`: genera el planner de 100 páginas con pestañas y enlaces internos.
- Generados 3 PDF (sage, blush, mono) y 4 imágenes para la ficha de venta.
- Escrita la ficha completa en `products/planner-2027/LISTING.md` (título, 13 etiquetas, descripción y precio).

## Ciclo 2 — 2026-11-17 22:30 UTC
- Creado `tools/budget2027.py`: hoja de cálculo de presupuesto 2027 para Excel y Google Sheets. Incluye categorías editables, 12 meses con desplegables, presupuesto vs. real, dashboard con 2 gráficos, metas de ahorro y calculadora de deudas.
- Fórmulas verificadas recalculando con LibreOffice: 0 errores y totales correctos con datos de prueba.
- Creadas 4 imágenes para la ficha y `products/budget-2027/LISTING.md`.

## Ciclo 3 — 2026-11-17 23:30 UTC
- Creado `tools/wallart.py`: genera láminas boho en 5 proporciones de impresión (2:3, 3:4, 4:5, 11x14, ISO) a 300 DPI.
- 2 sets de 6 diseños originales: abstracto (arcos, arcoíris, sol, tallo botánico) y afirmaciones con frases propias.
- Corregidos 2 diseños tras revisarlos visualmente.
- Imágenes de ficha: cuadros enmarcados en una pared, cuadrícula de los 6 diseños y tabla de tamaños.
- Fichas completas en `products/wall-art/LISTING.md`.

## Ciclo extra (pedido del usuario: adelantar KDP) — 2026-11-18
- Añadido el modo `--print` a `tools/planner2027.py`: sin pestañas ni enlaces, márgenes espejo con medianil de 0.75", en escala de grises para impresión en blanco y negro (la más barata), y todas las fuentes incrustadas (KDP lo exige).
- Creado `tools/kdp_cover.py`: portada completa según la fórmula oficial de KDP (lomo = páginas × 0.002252", sangrado de 0.125"). Para 100 páginas mide 17.4752 x 11.25 in.
- Guía completa en `products/kdp-planner-2027/KDP-UPLOAD.md`: título, subtítulo, descripción, 7 palabras clave, categorías, precio y declaración de IA.

## Ciclo 4 — 2026-11-18 00:30 UTC
- Creado `tools/budgetbook2027.py`, que reutiliza el motor del planner. Genera el libro de presupuesto de 100 páginas: resumen financiero, panorama anual, control de facturas, 12 presupuestos mensuales, 48 páginas de gastos, 12 revisiones mensuales con días sin gasto, ahorro, fondos de ahorro por objetivo, deudas y notas.
- Pasé de 80 a 100 páginas para que el texto del lomo se pueda leer.
- `tools/kdp_cover.py` ahora genera portadas de distintos libros con `--book planner|budget`. Comprobé que la portada del planner sigue idéntica.
- Guía en `products/kdp-budget-2027/KDP-UPLOAD.md`.

## Ciclo 5 — 2026-11-18 01:30 UTC
- `tools/wallart.py` tiene un nuevo modo `TRANSPARENT`. `tools/pod.py` lo usa para exportar 12 PNG transparentes, recortados y centrados en un lienzo de 4500x5400.
- Guía de subida a Redbubble y Teepublic con título y 15 etiquetas por diseño, en `products/pod-redbubble/UPLOAD.md`.
- Nota: los diseños con texto oscuro solo deben venderse en colores claros.

## Ciclo 6 — 2026-11-18 02:30 UTC
- Creado `tools/site.py`: genera un sitio estático en `/docs` para GitHub Pages con SEO básico (metadatos, canonical, sitemap y robots). Tiene 5 páginas: inicio, calendario 2027 imprimible gratis (2 PDF), calculadora de presupuesto 50/30/20, calculadora de deudas (bola de nieve vs. avalancha) y calculadora de metas de ahorro.
- Cada página tiene un recuadro que enlaza a los productos; los enlaces se configuran en `SHOP`.
- Probado en navegador sin interfaz con ancho de móvil: 0 errores, sin desbordamiento horizontal, cálculos correctos.

## Ciclo 7 — 2026-11-18 03:30 UTC
- Sin acciones del usuario todavía, así que prioricé el tráfico del sitio. Añadí 12 páginas "<Mes> 2027 Calendar" con un PDF por mes, una tabla del calendario en la página y los feriados de EE. UU. calculados por reglas (Pascua con el algoritmo de Gauss). Verificadas contra las fechas reales.
- Probadas en tamaño de celular: 0 errores y sin desbordamiento. El sitio pasa a tener 17 páginas en el sitemap.

## Ciclo 8 — 2026-11-18 04:30 UTC
- No se puede verificar desde aquí si GitHub Pages está activo: el proxy de la sesión bloquea github.io.
- Añadí `dark_variants()` en `tools/pod.py`: 6 versiones de las frases con texto crema para ropa oscura. Instrucciones añadidas en `UPLOAD.md` (obras separadas, solo ropa oscura).

## Ciclo 9 — 2026-11-18 05:30 UTC
- Sin respuesta del usuario desde hace unas 5 horas. El cuello de botella ahora es publicar, no crear más productos.
- Creé `START-HERE.md`: una única checklist ordenada por impacto, con tiempos estimados y rutas de archivos (KDP, Pages, Redbubble y Etsy).

## Ciclo 10 — 2026-11-18 06:30 UTC
- Ficha de paquete para Etsy: planner + hoja de presupuesto por USD 10.99 (ahorro del 25%). Kit en `products/bundle-2027/`, con imagen principal.

## Ciclo 11 — 2026-11-18 07:30 UTC
- Sin acciones del usuario (unas 7 horas). No creé productos nuevos: hacer más sin publicar nada aporta poco. Solo correo breve.
