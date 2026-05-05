# GGSR Hugo Site

Sitio estático del Grupo de Geodesia Satelital de Rosario (FCEIA, UNR), migrado desde Nikola. Destino: **Netlify** (en proceso de configuración).

## Contexto de la migración

Sitio original: `/home/santi/devel/ggsr_site` (Nikola, RST + Textile, tema Cosmo/Bootstrap 4).  
El servidor original en `fceia.unr.edu.ar` solo tiene acceso FTP, lo que hacía difícil el mantenimiento.

La conversión de páginas se hizo con pandoc vía Docker (`pandoc/core`) desde RST/Textile a Markdown GFM. El script está en `tools/convert.py` — útil si hay que re-convertir algo.

## Comandos

```bash
hugo server          # servidor local en http://localhost:1313
hugo build           # build en ./public/
```

Para convertir páginas (requiere Docker con imagen `pandoc/core`):
```bash
python3 tools/convert.py
```

Para actualizar el mapa de estaciones TR (genera GeoJSON en `static/mapatr/`):
```bash
python3 tools/mapatr/fetch_sourcetables.py
```

## Estructura

```
content/       # páginas en Markdown (una por página del sitio)
layouts/       # templates HTML propios (sin tema externo)
  _default/
    baseof.html    # base: navbar + Bootstrap 5 CDN + CSS propio + footer
    single.html    # layout de página individual (envuelve en .ggsr-content)
  index.html       # layout del homepage (hero + 3 cards hardcodeadas)
  partials/
    navbar.html    # barra de navegación (navbar-light bg-white)
static/
  assets/css/
    custom.css     # estilos propios: paleta institucional, navbar, hero, cards, footer
  mapatr/          # mapa de estaciones tiempo real
    map.html       # página del mapa (Leaflet 1.9, carga GeoJSON estáticos)
    *.geojson      # datos de cada caster (generados por fetch_sourcetables.py)
    BASE.geojson   # estaciones base fijas
    src/js/map.js  # lógica Leaflet: capas, popups, layer control
    src/css/map.css
  ...              # PDFs, imágenes, etc.
tools/
  convert.py            # script de migración Nikola → Hugo (para referencia)
  mapatr/
    fetch_sourcetables.py  # descarga sourcetables NTRIP y genera GeoJSON
                           # usa socket raw (protocolo NTRIP no es HTTP estándar)
                           # sin dependencias externas (solo stdlib Python 3)
.github/workflows/
  deploy.yml            # build + deploy a Netlify (o GH Pages si se cambia)
  update-mapatr.yml     # cron diario: actualiza GeoJSON y commitea
```

## Diseño

Bootstrap 5.3 desde CDN (jsDelivr) + `static/assets/css/custom.css`. Sin dependencias de Node/npm ni tema externo.

**Paleta:**
- Acento: `#1b5e8a` (azul institucional)
- Fondo alternado: `#f5f7f9`
- Footer: `#2c3e50`

**Navbar:** blanco con borde superior de 4px en color acento. Clases Bootstrap: `navbar-light bg-white`.

**Homepage:** sección hero (contenido de `_index.md`) + 3 cards hardcodeadas en `layouts/index.html`.

**Páginas internas:** contenido en `<article class="ggsr-content">` con max-width 800px y h2 con borde izquierdo de acento.

Para cambiar colores o tipografía: editar `static/assets/css/custom.css`.  
Para cambiar las cards del homepage: editar `layouts/index.html`.

## Mapa de estaciones TR (`/mapatr/`)

El mapa muestra qué casters NTRIP están activos y qué estaciones transmiten en tiempo real.

**Estado actual:** carga GeoJSON pre-generados (actualizados por cron diario vía GitHub Actions). El objetivo es migrarlo a **Netlify Functions** para consulta en tiempo real al cargar la página.

**Por qué no se puede consultar directo desde el navegador:** los casters NTRIP usan un protocolo propio (responden con `SOURCETABLE 200 OK` en lugar de `HTTP/1.1 200 OK`), no tienen cabeceras CORS, y el sitio en HTTPS no puede hacer requests a HTTP (mixed content).

**Casters consultados:**

| Nombre | Host | Color |
|--------|------|-------|
| IGS-RT | www.igs-ip.net:2101 | rojo |
| IBGE-IP (Br) | gps-ntrip.ibge.gov.br:2101 | verde |
| REGNA-SGM (Uy) | 201.217.132.178:2101 | celeste |
| RAMSAC-NTRIP (Ar) | ntrip.ign.gob.ar:2101 | azul |

## Pendiente / issues conocidos

### Crítico para el deploy
- [ ] **Migrar a Netlify**: configurar repo en GitHub, conectar a Netlify, ajustar `netlify.toml` y `baseURL` en `hugo.toml`.
- [ ] **Netlify Function para mapatr**: función Python/Node que proxy-ea las consultas a los casters NTRIP en tiempo real. El `map.js` deberá llamar a `/.netlify/functions/ntrip?caster=IGN` en lugar de cargar archivos GeoJSON estáticos.

### Correcciones de contenido
- [ ] **`publicaciones.md`**: algunos links del Textile no convirtieron bien (el formato `"texto":referencia` con `[referencia]/url/`). Revisar la sección "2015" y otras.
- [ ] **`contacto.md`**: el email aparece en texto plano. Ver si se quiere proteger contra scrapers.
- [ ] **`librogps.md`**: apunta a `/librogps/` que era una aplicación web separada. Verificar si ese recurso sigue disponible.

### Páginas para revisar
- `content/index-old.md` — versión vieja del index, no necesita estar en producción. Borrar o archivar.

## Cómo agregar/editar contenido

Cada página es un archivo `.md` en `content/`. El front matter mínimo:

```yaml
---
title: "Título de la página"
slug: "url-de-la-pagina"
---
```

El campo `notitle: true` en el front matter suprime el `<h1>` automático (usado en el homepage).

La navegación se define en `hugo.toml` bajo `[[menus.main]]`, no se genera automáticamente.
