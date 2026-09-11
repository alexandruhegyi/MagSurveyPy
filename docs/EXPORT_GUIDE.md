# MagSurveyPy 1.0.3 — Export and Cartography Guide

MagSurveyPy separates quantitative scientific rasters from their presentation. `export map` and `figure` change only how a product is drawn; they do **not** rewrite magnetic values.

Use the short launcher shown below when configured:

```bash
mspy ...
```

`mspy ...` remains fully equivalent.

## Publication map

```bash
mspy export map \
  --project Site \
  --from INTERPOLATED \
  --display-range 15
```

### Magnetic legend

The magnetic legend can be placed on the right or bottom and its text can be fully customized.

```bash
--colorbar-position right
--colorbar-label-size 8
--colorbar-tick-size 7
--colorbar-thickness 0.10
```

Colourbar end labels are pinned to the actual display limits. For example, a magnetic display range of **−10 to +10 nT** always prints `−10` at the lower/left end and `10` at the upper/right end of the colourbar. Automatic tick spacing only controls the intermediate labels; it can never move, omit, or extend beyond the requested endpoints.

Override only the text inside parentheses:

```bash
--magnetic-unit nT/m
--magnetic-unit nT
--magnetic-unit "custom unit text"
```

Change the text before the parentheses:

```bash
--magnetic-label "Magnetic anomaly"
```

Or replace the complete legend label:

```bash
--colorbar-label "Vertical magnetic gradient (nT/m)"
```

### Typography

```bash
--title-size 12
--axis-label-size 9
--tick-label-size 7
--colorbar-label-size 8
--colorbar-tick-size 7
```

The grid can be independently styled:

```bash
--grid-width 0.4
--grid-alpha 0.30
```

### Scale bar

Scale bars can be inside or outside the map frame, aligned left/center/right, and placed at the top or bottom.

Example:

```bash
--scale-bar \
--scale-bar-position outside-bottom-center \
--scale-bar-style blocks \
--scale-bar-length auto \
--scale-bar-segments 4 \
--scale-bar-font-size 6.5 \
--scale-bar-box \
--scale-bar-box-alpha 0.85
```

Supported positions:

```text
inside-bottom-left      inside-bottom-center      inside-bottom-right
inside-top-left         inside-top-center         inside-top-right
outside-bottom-left     outside-bottom-center     outside-bottom-right
outside-top-left        outside-top-center        outside-top-right
```

Styles:

```text
blocks   alternating black/white segments
line     thin metric line with ticks
simple   single filled bar with ticks
```

The first and last labels are aligned inward. When the scale box is enabled, label drawing is clipped to the scale container so labels do not extend beyond the box.

A fixed total length can be requested in metres:

```bash
--scale-bar-length 50
```

### North arrow

```bash
--north-arrow \
--north-position outside-top-right \
--north-size 0.11 \
--north-box \
--north-box-alpha 0.55
```

North-arrow positions use the same inside/outside position names as the scale bar. The arrow always represents north; the position can be top/bottom/left/right, but its direction is not arbitrarily rotated.

### Coordinate axes

Projected coordinates:

```bash
--axis-mode coordinates
```

Local metric distance axes:

```bash
mspy export map --project Site --from INTERPOLATED \
  --axis-mode distance \
  --grid-distance-x 25 \
  --grid-distance-y 25
```

No axis annotation:

```bash
--axis-mode none
```

### Basemap and attribution

```bash
mspy export map \
  --project Site \
  --from INTERPOLATED \
  --basemap esri-satellite
```

The basemap remains below the magnetic raster. **MagSurveyPy branding is off by default.** Add `--mspy-credit` when you want the version-neutral MagSurveyPy logo in the footer; its position, size and opacity can be adjusted. Basemap/provider attribution is independent: it is shown by default when a basemap is used, placed unobtrusively **below the right side of the map**, and can be suppressed with `--no-basemap-credit` where your provider licence/publication workflow permits.


### Optional MagSurveyPy logo and provider attribution

No MagSurveyPy branding is added to maps/figures unless explicitly requested. To add the version-neutral logo:

```bash
mspy export map --project Site --from INTERPOLATED \
  --mspy-credit \
  --mspy-credit-position bottom-left \
  --mspy-credit-size 0.10 \
  --mspy-credit-alpha 1
```

The supplied `assets/magsurveypy_logo.png` contains **no version number** so it remains suitable across releases.

Provider attribution is independent. It is enabled by default when a basemap is used:

```bash
--basemap-credit
```

To suppress it where licensing permits:

```bash
--no-basemap-credit
```

When enabled, provider attribution is placed in the footer and only adds the space required by the text; it does not create a white map-corner block.

### Full customized example

```bash
mspy export map \
  --project Rupea \
  --from INTERPOLATED \
  --display-range 10 \
  --cmap gray_r \
  --title "Rupea magnetic survey" \
  --title-size 12 \
  --axis-label-size 9 \
  --tick-label-size 7 \
  --magnetic-label "Magnetic gradient" \
  --magnetic-unit "nT/m" \
  --colorbar-position right \
  --colorbar-label-size 8 \
  --colorbar-tick-size 7 \
  --scale-bar-position outside-bottom-center \
  --scale-bar-style line \
  --scale-bar-box-alpha 0.75 \
  --north-position outside-top-right \
  --north-box-alpha 0.45 \
  --dpi 600 \
  --format pdf
```

## Publication figures

`figure single` accepts the same cartographic and typography options. Scale bar and north arrow are optional for a plain scientific figure:

```bash
mspy figure single \
  --project Rupea \
  --from INTERPOLATED \
  --display-range 10 \
  --scale-bar \
  --scale-bar-position inside-top-center \
  --north-arrow \
  --north-position inside-bottom-right \
  --magnetic-unit nT/m \
  --format pdf
```

For flexible multi-panel layouts use `figure template` + `figure build`; see `FIGURE_BUILDER_GUIDE.md`.

## Reproject

```bash
mspy export reproject --project Site --from INTERPOLATED --epsg 4326
```

## Contours

```bash
mspy export contours \
  --project Site --from INTERPOLATED \
  --interval 1 --format gpkg
```

## Dissemination bundle

```bash
mspy export bundle --project Site --from INTERPOLATED
```

The quantitative GeoTIFF remains the scientific data product. Figures, maps and basemaps are presentation/dissemination products.

---

**MagSurveyPy 1.0.3** — Developed by **Alexandru Hegyi, PhD**
https://alexandruhegyi.com · alexandruhegyi@gmail.com · https://github.com/alexandruhegyi
