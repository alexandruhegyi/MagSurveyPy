# MagSurveyPy 1.0.1 — Publication Figure Builder

The `figure` group is intended for papers, reports, supplementary data and processing comparisons. It never modifies the quantitative source raster.

## Single publication figure

```bash
mspy figure single \
  --project Rupea \
  --from INTERPOLATED \
  --display-range 15 \
  --cmap gray_r \
  --colorbar-position right \
  --format pdf
```

`figure single` supports the same publication controls as `export map`, including:

- title, axis and tick sizes;
- magnetic legend wording and unit override;
- thin right/bottom colorbars;
- optional scale bar inside/outside the frame;
- optional north arrow inside/outside the frame;
- scale/north boxes and opacity;
- scale style, length, segments and label size;
- grid width/opacity;
- optional version-neutral MagSurveyPy logo credit (off by default).

Example:

```bash
mspy figure single \
  --project Foeni \
  --from TOTAL_FIELD \
  --display-range 20 \
  --magnetic-label "Magnetic anomaly" \
  --magnetic-unit nT \
  --title-size 11 \
  --axis-label-size 8 \
  --tick-label-size 7 \
  --scale-bar \
  --scale-bar-position outside-bottom-center \
  --scale-bar-style line \
  --north-arrow \
  --north-position outside-top-right \
  --format pdf
```

## Compare processing stages

```bash
mspy figure compare \
  --project Rupea \
  --stages NATIVE,INTERPOLATED,CLEAN \
  --display-range 15 \
  --colorbar-position bottom
```

The maps use a common scale and quantitative difference/statistics are written alongside the figure.

## Flexible multi-panel recipe figures

Create a template:

```bash
mspy figure template \
  --project Rupea \
  --preset publication \
  -o rupea_publication.json
```

Edit the JSON, then build:

```bash
mspy figure build \
  --project Rupea \
  --recipe rupea_publication.json \
  -o Rupea_Figure_4.pdf
```

Supported panel types:

```text
raster          magnetic raster
difference      difference between compatible rasters
histogram       magnetic-value distribution
spectrum        spatial power spectrum
line-summary    line/traverse QC
sensor-summary  sensor/channel QC
image           existing illustration/graph
text            notes, methods or caption content
```

## Styling JSON recipes

The `shared` block controls default typography and credits:

```json
{
  "shared": {
    "title_size": 12,
    "axis_label_size": 8,
    "tick_label_size": 7,
    "colorbar_label_size": 8,
    "colorbar_tick_size": 7,
    "credit_size": 0.10,
    "credit_position": "bottom-left",
    "credit_alpha": 1.0,
    "credits": false
  }
}
```

Individual raster panels can override those defaults and can also contain map elements:

```json
{
  "type": "raster",
  "source": "INTERPOLATED",
  "title": "Magnetic gradient",
  "display_range": 10,
  "cmap": "gray_r",
  "magnetic_label": "Magnetic gradient",
  "magnetic_unit": "nT/m",
  "colorbar": true,
  "colorbar_position": "right",
  "colorbar_label_size": 8,
  "colorbar_tick_size": 7,
  "colorbar_thickness": 0.10,
  "scale_bar": true,
  "scale_bar_position": "inside-bottom-left",
  "scale_bar_style": "blocks",
  "scale_bar_segments": 4,
  "scale_bar_font_size": 6.2,
  "scale_bar_box": true,
  "scale_bar_box_alpha": 0.82,
  "north_arrow": true,
  "north_position": "inside-top-right",
  "north_size": 0.10,
  "north_box": true,
  "north_box_alpha": 0.50
}
```

The exact JSON template written by the installed build is the safest starting point.

## Publication recommendations

- Use a common display range when visually comparing magnetic rasters.
- Keep **nT** and **nT/m** explicit.
- Use difference panels when assessing what a processing step removed.
- Prefer PDF/SVG for vector text and axes when accepted by the journal.
- Preserve the JSON recipe with the paper/project so the figure can be rebuilt.
- Do not use display clipping to imply that magnetic amplitudes were physically rescaled.

---

**MagSurveyPy 1.0.1** — Developed by **Alexandru Hegyi, PhD**
https://alexandruhegyi.com · alexandruhegyi@gmail.com · https://github.com/alexandruhegyi
