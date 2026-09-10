# Validation — MagSurveyPy Version 1.0.0

## SENSYS processing regression

The processing core remains based on the validated SENSYS/MonMX PRM workflow: native FGM fine/coarse magnetic-word decoding, PRM-header initial GPS allocation, per-block GPS positioning, physical probe geometry, authoritative ASC generation and supported small-gap interpolation with larger acquisition gaps left NoData.

## Cartographic export regression

The current release was exercised on an EPSG:32635 Rupea GeoTIFF for:

- `figure single`;
- `export map` with full Easting/Northing coordinates;
- `export map --axis-mode distance --grid-distance-x 25 --grid-distance-y 25`;
- map-view zoom behavior;
- `export reproject`;
- `export contours`;
- `figure compare`;
- `export bundle`.

The cartographic export system supports scale bars inside or outside the map at top/bottom and left/center/right positions, with `blocks`, `line` and `simple` styles, configurable segment count/length, font size, optional background box and transparency. Edge labels are aligned inward and clipped to their scale container so they do not extend outside the box. North-arrow placement/size/background are independently configurable. Projected Northing tick labels are written as full coordinate values and rotated vertically rather than using Matplotlib offset notation. Magnetic colourbars are product-aware (**nT** or **nT/m**) and their label/unit text, typography, thickness and placement can be customized.

MagSurveyPy branding is absent by default from exported maps/figures; optional branding uses the version-neutral logo. Esri/basemap attribution is independently switchable and, when enabled, is placed below the right side rather than inside a map corner. Bottom colourbars, outside-bottom scale bars and enabled footer elements use collision-aware stacking. `--zoom` changes the complete map extent, not only tile resolution, so basemap and magnetometry scale together.

The public static-map basemap choices are deliberately limited to:

```text
none
esri-satellite
```

Live online satellite download depends on the installation environment and internet access. `requirements.txt` and `environment.yml` contain `contextily` and `xyzservices`; the package itself was validated with no-basemap rendering in the packaging environment when `contextily` was unavailable.

## Web GIS API regression

The local Web GIS server was exercised against the Rupea test project. The following behavior was tested:

- `/api/layers` returns important project layers only by default;
- `/api/project-files` lists additional addable GIS files without loading them automatically;
- dynamic raster PNG rendering;
- cumulative-cut and standard-deviation raster stretch logic;
- profile sampling along an interactively defined line with distance in metres and values in nT/m;
- project vector registration;
- local GeoJSON upload and dynamic layer registration;
- drawing save to GeoPackage;
- drawing save to zipped ESRI Shapefiles;
- export of a deliberately cropped current Web GIS canvas extent (not the whole survey) using the exact browser bounds and browser canvas aspect ratio, with selected raster style and drawing geometry;
- profile endpoint sampling for a multi-vertex line;
- GeoPackage drawing save;
- browser basemap configuration for Esri Satellite, OpenStreetMap, Esri Topographic and custom WMS/WMTS/XYZ.

A test profile returned 1,200 samples over approximately 190.6 m. The current-view export produced a publication PNG with full coordinate axes, configurable scale bar/north arrow, product-aware magnetic colourbar and the supplied drawing geometry. Web navigation uses fractional 0.25 zoom steps for finer framing.

The Web GIS is display/export oriented: it never rewrites the scientific rasters in `Results/`.

## Browser-side validation

The embedded Web GIS JavaScript was syntax-checked with Node.js after substituting a valid project metadata payload. The geometry manager no longer contains Leaflet.Draw or `L.EditToolbar` state; creation/editing is implemented with Leaflet-Geoman and per-feature selection. Server-side profile, drawing and cropped-current-extent export APIs were exercised directly. Browser-loaded Leaflet/Leaflet-Geoman and online basemap providers still require normal network access.

## Installation validation

The final environment files include the standard numerical/GIS stack plus `geopandas`, `pyogrio`, `contextily` and `xyzservices`, so normal raster/vector import/export, GeoPackage/Shapefile writing and static online cartography can be installed from one environment definition.

## 1.0.0 Web GIS / cartography refinement validation — 8 September 2026

The 1.0.0 refinement was checked with a synthetic georeferenced EPSG:32634 raster in both tall and wide survey geometries.

Validated items:

- `mspy --version` and the compatibility `multimag.py --version` both render the MagSurveyPy banner and explicit 1.0.0 version line.
- Python sources compile with `python -m py_compile`.
- Embedded Web GIS JavaScript parses successfully with Node `--check` after template substitution.
- The local Web GIS serves its HTML and `/api/layers` state from the standard-library threaded HTTP server.
- A real threaded `/api/export-map` request was executed against a synthetic EPSG:32634 project using the headless Agg backend; Ctrl+C shutdown returned code 0 with no Matplotlib GUI-thread warning, no `inotify_add_watch` message and no segmentation fault in the test environment.
- Web drawing persistence endpoints write mixed point/line/polygon drawings to GeoPackage and zipped Shapefiles.
- Static `figure single` and `export map` complete with both `--colorbar-position right` and `--colorbar-position bottom`.
- Web GIS current-view export completes with both vertical-right and horizontal-bottom colourbar placements.
- Tall and wide rendered-map tests confirm that right colourbars follow map height, bottom colourbars follow map width, and bottom bars reserve separate space below X-axis labels.

Interactive geometry code uses Leaflet-Geoman 2.20.0 with one-shot creation and per-feature editing rather than global edit/delete sessions. Static checks verify that Leaflet.Draw/`L.EditToolbar` references are absent, drawing clicks stop propagation before the map deselection handler, and Escape/Cancel reverts unfinished edits. Full browser interaction still depends on the browser being able to load the JavaScript libraries.
Colourbar validation also requires the exact requested vmin/vmax labels to appear at the physical ends of both vertical and horizontal quantitative colourbars (e.g. −10 and +10 for a −10…+10 nT display range).

- Exact quantitative colourbar endpoint regression: `--display-min -10 --display-max 10` renders -10 and +10 at the physical bar ends in vertical and horizontal orientations.
- Display-only tone regression: brightness, contrast, gamma and saturation alter rendered maps/figures/Web GIS output without changing source GeoTIFF checksums/statistics.
- Export-credit regression: MagSurveyPy branding is absent by default; `--mspy-credit` uses the version-neutral logo; basemap/provider attribution is independently switchable.
