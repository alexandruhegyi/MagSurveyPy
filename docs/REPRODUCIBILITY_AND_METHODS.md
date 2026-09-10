# Reproducibility and Methods Reporting

For a journal manuscript or archived survey, MagSurveyPy should be treated as a reproducible processing pipeline rather than only a map-making tool.

## Record at minimum

- MagSurveyPy version (`mspy --version`).
- Instrument and acquisition geometry.
- Coordinate reference system.
- Imported raw-data identity/provenance.
- Exact `survey` command and non-default parameters.
- Interpolation method/cell size/support policy.
- Any `filter` command and why it was applied.
- Analysis outputs used to justify a correction.
- Figure display range/colormap and figure recipe.

## Preserve reference and derived branches

For total-field surveys, distinguish absolute corrected field from archaeology residuals. For fluxgate/gradiometer grids, distinguish assembled measured gradient from any levelled/zero-centred derived branch.

## Report processing as operations, not appearance

Prefer:

> Traverse baselines were removed using robust per-line centering, followed by a 10 m Gaussian background subtraction on the archaeology branch.

rather than:

> The map was cleaned until the stripes disappeared.

## Display range is not processing

A figure displayed at ±10 nT or ±20 nT has not been numerically rescaled by MagSurveyPy. Report quantitative filtering separately from visual stretch.

## Suggested archive contents

```text
project.json / project configuration
RawData provenance or checksums
Results quantitative GeoTIFF/ASC products
Reports/Analysis
filter audit JSON + removed components
figure recipe JSON
final figure/map exports
environment.yml or dependency record
command history / methods text
```

## Georeferencing provenance

Every control-point georeferencing operation writes the fitted control points and residuals to `.gcps.csv` and the complete affine transform, CRS, source/output paths, RMSE and software version to `.georef.json`. The initial georeferencing operation explicitly records `values_resampled: false`. If a later reprojection is needed, use `export reproject` as a separate command so the spatial resampling step appears explicitly in the workflow history.

## Automatic command provenance

Project-scoped CLI invocations are recorded under `Project/Logs/`. The exact shell-ready command is written to the master history and to a command-group log, while `command_status.tsv` records completion state and duration. This makes the sequence used to produce a published result recoverable without embedding command history inside the quantitative raster itself.

When alternative processing or cartographic variants need to coexist, use `--increment` to create a numbered output rather than replacing the normal target. This is preferable for controlled method comparisons because the original result and its command remain available together.
