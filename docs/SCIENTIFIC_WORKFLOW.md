# Scientific Workflow

MagSurveyPy 1.0.0 uses a workflow that keeps original/reference data separate from derived products in which every command group has a defined scientific role.

```text
RAW FIELD DATA
     ↓
PROJECT provenance and configuration
     ↓
SURVEY instrument-aware decoding/correction
     ↓
ANALYZE acquisition geometry, lines, sensors, distribution, spectrum
     ↓
PROCESS core derived stage (interpolate / clean / enhance / segment / thin)
     ↓
FILTER only if a diagnosed correction is scientifically justified
     ↓
ANALYZE again + inspect removed/difference products
     ↓
FIGURE reproducible publication/analysis panels
     ↓
EXPORT GIS/cartography   or   WEB interactive interpretation
```

## Preservation before residual processing

MagSurveyPy retains reference/quantitative products before archaeology-only transformations where the instrument branch requires this. This is particularly important for scalar total field: an archaeology residual centred around 0 nT must not replace the corrected absolute-field product.

## Interpolation is not acquisition correction

Interpolation estimates a spatial surface from supported observations. It should not be used to conceal gaps, stripes, line offsets or poor acquisition geometry. Large unsupported gaps remain NoData by default.

## Filtering requires a hypothesis

Use `analyze` first. Apply a filter because a line offset, wavelength component, regional trend or directional stripe is diagnosed—not simply because a processed image appears visually smoother.

## Publication requires reproducibility

Use common display ranges for comparisons, preserve removed components, save analysis reports and keep the JSON recipe used by `figure build` with the project/manuscript.
