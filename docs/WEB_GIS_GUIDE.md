# MagSurveyPy 1.0.0 — Web GIS Guide

## Launch

```bash
mspy web --project Site
```

Equivalent fallback:

```bash
mspy web --project Site
```

MagSurveyPy starts a responsive local Web GIS on `127.0.0.1:8050`. Stop it with `Ctrl+C`.

## Workspaces

- **Layers** — visibility, ordering, imports and layer properties;
- **Map** — basemap, opacity/brightness and fine navigation;
- **Analysis** — quantitative multi-vertex magnetic profiles;
- **Georef** — control-point georeferencing of unreferenced rasters;
- **Draw** — point/line/polygon creation and per-feature editing;
- **Export** — exact-current-canvas publication export.

The Web GIS displays MagSurveyPy 1.0.0 and developer/contact credits in the application interface and About dialog.

## Fine zoom

Web navigation uses **0.25 zoom-level increments** rather than only whole Leaflet zoom levels. The +/- buttons also use 0.25 steps. This is useful for framing narrow archaeological surveys precisely.

## Raster properties

Raster display styling is non-destructive and includes:

- manual min/max;
- standard-deviation stretch;
- cumulative tail cuts;
- full-data range;
- colour map;
- opacity;
- blend mode;
- brightness;
- contrast;
- gamma;
- saturation.

These are display-only tone controls. The Web GIS requests a transformed display colour map while retaining the original magnetic raster values and exact numeric stretch limits.

Units are product-aware: scalar total-field products normally use **nT**, while magnetic-gradient products normally use **nT/m**.

## Magnetic profile

Choose a quantitative raster and draw a multi-vertex profile. The graph reports:

- cumulative distance in metres;
- source-raster magnetic units;
- true NoData gaps;
- min/max/mean/median/standard deviation;
- zero and median reference lines when relevant;
- hover distance/value;
- CSV export whose column name follows the raster unit.

Profile sampling is read-only.

## Drawing editor

Point, line and polygon creation uses Leaflet-Geoman. Creation is one-shot. Finished features can be selected individually, double-clicked to edit, saved with Enter, reverted with Escape, or deleted individually.

Drawings can be saved as GeoPackage or zipped Shapefile under:

```text
Project/Exports/WebGIS/Drawings/
```

## Georeferencing

Unreferenced magnetic TIFFs can be fitted from 3+ image/GPS control points. The tool writes a georeferenced quantitative GeoTIFF without changing magnetic values and stores GCP/residual provenance beside it. See `GEOREFERENCING_GUIDE.md`.

## Exact-current-canvas export

The export request sends **both the exact Leaflet bounds and the actual browser map-canvas width/height** to the server. The renderer uses those values to reproduce the visible map framing rather than independently fitting the survey.

The Web GIS export panel now controls:

### General layout

- title text and size;
- DPI and format;
- coordinate/distance/no-axis mode;
- axis label size;
- tick label size;
- grid interval, line width and opacity.

### Magnetic legend

- show/hide;
- right or bottom placement;
- text before the unit;
- arbitrary text inside parentheses (`nT/m`, `nT`, or any custom text);
- complete label override;
- label/tick sizes;
- bar thickness.

### Scale bar

- show/hide;
- inside/outside frame;
- top/bottom and left/center/right placement;
- blocks, line or simple style;
- automatic or fixed metric length;
- 1–8 segments;
- label size;
- box on/off and transparency.

The edge labels face inward. When a box is used, labels are constrained to the scale container and are not allowed to extend past it.

### North arrow

- show/hide;
- inside/outside frame;
- top/bottom and left/right placement;
- size;
- box on/off and transparency.

### Credits

Exported maps contain **no MagSurveyPy credit by default**. The export panel has a `Show MagSurveyPy logo` option; when enabled it inserts the version-neutral logo with configurable position, size and opacity. Basemap/Esri attribution is controlled separately with `Show basemap / Esri attribution`. When enabled, attribution is printed gracefully below the right side instead of inside an isolated white corner. The browser map also has a separate attribution-visibility toggle. Provider attribution should only be disabled where licensing permits.

## Output

```text
Project/Exports/WebGIS/Maps/
```

PNG, PDF and SVG are supported.

## Scientific policy

Web styling, basemaps, profiles, drawings and publication export never rewrite quantitative `Results` rasters.

---

**MagSurveyPy 1.0.0** — Developed by **Alexandru Hegyi, PhD**  
https://alexandruhegyi.com · alexandruhegyi@gmail.com · https://github.com/alexandruhegyi


## Precision raster georeferencing

The **Georef** workspace uses an independent zoomable raster editor. Use **Fit**, **100%**, **Zoom −**, **Zoom +**, or **Ctrl + mouse wheel** to inspect control-point locations. When zoomed in, pan with the preview scrollbars.

GCP clicks are continuous sub-pixel raster coordinates and are never snapped. The preview image and marker overlay share the same raster stage and transformation, so a marker remains at the exact clicked position regardless of zoom or scrolling. Pixel X/Y values can also be edited numerically to 0.001 pixel in the GCP table.

Georeferencing still fits one least-squares affine transform from all entered points and writes the source magnetic values unchanged to the new GeoTIFF.
