# MagSurveyPy 1.0.1 — Functions and Results Reference

Developed by **Alexandru Hegyi, PhD**.

This document explains what the supported public functions do and what the main predefined products mean. It is intended for users who want to understand the scientific outputs without reading the Python source.

## 1. Scientific separation used by MagSurveyPy

MagSurveyPy separates four things:

1. **Raw observations** — original instrument files in `RawData/`.
2. **Scientific results** — quantitative derived products in `Results/`.
3. **QC/analysis** — diagnostic statistics and graphs in `Reports/`.
4. **Presentation/export** — maps, figures and GIS deliverables in `Exports/`.

Display ranges, colour maps, scale bars, north arrows and basemaps do not modify the scientific raster.

## 2. Project functions

### `project init`
Creates the project structure and `project.json` metadata.

### `project import`
Copies or links source field data into the appropriate `RawData` branch. Original field data should remain unchanged.

### `project config`
Stores project defaults such as cell size, CRS or processing preferences.

### `project status`
Summarizes available raw inputs and result stages.

### `project georeference`
Fits an affine raster transform from 3+ image/GPS control points. Outputs:

- georeferenced GeoTIFF;
- `.gcps.csv` containing control points and residuals;
- `.georef.json` containing CRS, affine transformation, RMSE and provenance.

The initial georeferencing step assigns spatial geometry without resampling magnetic cell values.

## 3. Survey functions

### `survey prm`
Processes supported SENSYS/MonSX PRM data into an authoritative point/raster representation. Instrument geometry, probe channels, embedded positioning, acquisition blocks and QC are interpreted before gridding.

### `survey total-field`
Processes scalar total-field measurements in **nT**. The workflow can preserve an absolute/corrected field while separately creating an archaeology residual around zero. Important concepts include:

- **traverse zeroing** — line-wise baseline removal (`mean`, `median`, `robust`);
- **deslope** — broad linear/regional trend reduction;
- **protected destriping** — conservative line-pattern correction;
- **grid-level correction** — constant offset correction between separately acquired grids;
- **high-pass/background removal** — broad field component separated from local archaeological anomalies;
- **archaeology centering** — final residual centered around a robust baseline.

Absolute total-field products should not be confused with the archaeology residual.

### `survey grid --protocol fluxgate`
Processes supported fluxgate/gradiometer grid data in **nT/m**. Paired metadata/data grid formats are supported where implemented. Empty cells, saturation information, acquisition direction and local-grid assembly are handled separately from total-field processing.

### `survey generic`
Imports supported generic magnetic point/ASCII observations when instrument-specific interpretation is not required.

## 4. Layout functions

MagSurveyPy deliberately does **not** expose automatic layout inference as a supported public function. Local-grid placement must be explicit and reviewable.

### `layout validate`
Checks grid names, positions, rotations and consistency before assembly.

### `layout gui`
Interactive local-grid layout editor. The layout is explicit so MagSurveyPy does not silently guess archaeological grid positions.

## 5. Processing functions

### `process interpolate`
Constructs a supported surface while preserving larger unsupported acquisition gaps. Interpolation is not intended to conceal missing survey areas. The source may be supplied positionally or with `--input PATH`.

Example: `mspy process interpolate --project Site --input points.asc --method archaeology`

### `process clean`
Creates explicit archaeology-aware cleaning products. Where a correction removes signal, MagSurveyPy should retain the removed component/audit output so the user can inspect what changed.

### `process enhance`
Creates interpretative derivatives and multiscale products. Enhanced rasters are interpretation aids, not replacements for the quantitative reference.

### `process segment`
Creates candidate anomaly/object regions and vectors. Segmentation identifies geometrical candidates; it does not identify archaeological features by itself.

### `process thin`
Evaluates and optionally thins physically overlapping multisensor trajectories. QC distinguishes genuine unsupported gaps from gaps created by selection.

## 6. Filter functions

### `filter observations`
Operates on point/line observations before raster gridding. Typical uses:

- robust despiking;
- traverse/line zeroing;
- linear line drift removal;
- final robust centering.

### `filter raster`
Operates on an existing quantitative GeoTIFF. Project/stage selection or an explicit `--input RASTER` may be used. Typical filters include:

- Gaussian low-pass;
- median low-pass;
- high-pass/background removal;
- FFT wavelength filters;
- upward continuation;
- plane removal;
- directional stripe/notch filtering.

For comparison experiments, give each run a unique output/product name. A filter output should be treated as a new derived product rather than as a reason to discard the original raster.

## 7. Analysis functions

### `analyze survey`
Creates an overall survey/QC summary using available point and raster information.

### `analyze lines`
Examines line/traverse baselines, spread, sample count and sequence behaviour. Useful for diagnosing striping, line offsets or temporal drift.

### `analyze sensors`
Compares sensor/channel statistics. Useful for persistent channel bias, spread differences or a problematic sensor.

### `analyze raster`
Reports quantitative raster statistics and value distribution.

### `analyze spectrum`
Examines spatial wavelengths and directional spectral energy. It can identify a candidate stripe orientation, but the result is diagnostic and should be checked against acquisition direction and the map itself.

### `analyze stages`
Compares processing stages by common-cell statistics and correlation. This is useful for showing how much a processing stage changes the reference.

## 8. Figure functions

### `figure single`
One publication-quality magnetic raster figure. Supports exact colourbar limits, custom colorbar text/units, display-only brightness/contrast/gamma/saturation, typography, optional scale bar/north arrow and cartographic placement.

### `figure compare`
Common-scale comparison of multiple result stages plus difference rasters/statistics.

### `figure template` / `figure build`
Creates reproducible JSON-defined multi-panel figures combining magnetic rasters, differences, spectra, histograms, line/sensor graphs, images and text.

## 9. Export functions

### `export map`
Creates a cartographic map. It can add:

- coordinate or distance axes;
- grid;
- scale bar;
- north arrow;
- magnetic colorbar;
- optional basemap;
- optional version-neutral MagSurveyPy logo credit (off by default) and independently controlled basemap/provider attribution.

### `export reproject`
Resamples a quantitative raster into another CRS. Unlike simple GCP georeferencing, reprojection necessarily performs spatial resampling.

### `export contours`
Creates vector contours from a selected magnetic raster.

### `export bundle`
Collects quantitative raster, figure, map and reproducibility metadata for dissemination.

## 10. Web GIS functions

### Layer styling
Changes only visualization parameters, never the source GeoTIFF.

### Magnetic profile
Samples a quantitative raster along a user-drawn multi-vertex line. Distance is cumulative along the line. Values use the selected raster's unit.

### Drawing editor
Creates points, lines and polygons that can be edited and exported as GIS vectors.

### Georeferencer
Assigns spatial reference from image/GPS control points and reports residuals before writing.

### Exact-canvas export
Uses the current browser bounds and actual browser-canvas aspect ratio. This prevents export from independently refitting the entire survey after the user has framed a specific view.

## 11. Meaning of common predefined result stages

### `NATIVE`
Primary processed output closest to the supported instrument measurements and acquisition geometry. This is often the preferred quantitative reference for checking later processing.

### `TOTAL_FIELD`
Scalar total-field branch in **nT**. It may contain both preserved absolute/corrected field products and archaeology residual products. File/product names must be checked before interpretation.

### `FLUXGATE`
fluxgate/gradiometer branch in **nT/m**.

### `GEOREFERENCED`
A spatially referenced copy/result created from GCPs. Georeferencing provenance is stored beside it.

### `INTERPOLATED`
Supported gridded surface. Measured/observed support and larger NoData gaps remain scientifically important.

### `CLEAN`
Explicit cleaned/corrected branch. Compare it with its reference and removed-component products before using it as the sole interpretation map.

### `ENHANCED`
Interpretation derivative(s), e.g. multiscale/high-pass/edge-style products. These should be cited as derived products.

### `SEGMENT`
Candidate segmented regions/objects and vectors. These are analytical candidates rather than archaeological classifications.

## 12. Meaning of support and QC rasters

### Measurement / interpolation support `[0–1]`
Support expresses how close a cell is to real measured support relative to the configured interpolation distance.

For a fill distance `D` and nearest-observation distance `d`, the current support logic is:

```text
support = clip(1 - d / D, 0, 1)
```

Observed cells are forced to `1.0`.

Interpretation:

- `1.0` — directly observed/measured support;
- values between `0` and `1` — interpolation neighbourhood, progressively farther from measurement;
- `0` — outside the configured support distance.

A high-looking magnetic anomaly in a low-support region deserves more caution than the same anomaly in directly observed cells.

### Interpolation distance `[m]`
Distance from each grid cell to the nearest observed/measured cell. It answers: **how far did the surface have to reach to obtain support here?**

This is not magnetic amplitude and should not be displayed using nT/nT/m units.

### Measurement density
Number/weight of measurements contributing locally to the grid cell. Higher density can improve robustness, but repeated/overlapping measurements are not automatically equivalent to independent spatial coverage.

### Local noise
Local robust estimate of short-scale magnetic variability/noise. Units follow the magnetic product.

### Local SNR
Approximate local signal-to-noise ratio. Higher values indicate magnetic structure that is large relative to the estimated local noise. SNR is diagnostic; it is not an archaeological probability.

### Stability `[0–1]`
Agreement of anomaly behaviour across conservative processing/background choices. Higher values indicate that the anomaly persists across those choices. Stability does not prove archaeological origin.

### Removed component
The signal removed by a filter/correction. It is one of the most important audit products: if recognizable archaeological geometry appears strongly in the removed component, the correction may be too aggressive.

### Difference raster
Pixel-wise difference between two aligned stages. Used to quantify exactly what changed during processing.

### Sensor/channel statistics
Typically include count, median, robust spread and other diagnostics for each sensor/channel. Persistent sensor offsets can indicate calibration or leveling issues.

### Traverse/line statistics
Typically summarize line median/baseline, robust spread and sequence behaviour. Repeated alternating baselines commonly indicate acquisition striping.

### Spectrum / stripe candidate
The spectral analysis reports dominant wavelength behaviour and a candidate directional stripe orientation. It is diagnostic and should be compared with real traverse direction, plough direction and geology before applying a directional filter.

## 13. Display range versus scientific values

`--display-range 10` means a visualization approximately centered on the product baseline with a ±10-unit span. It does **not** rescale a 60 nT anomaly into 10 nT. Values outside the display range are clipped visually but remain unchanged in the quantitative raster.

## 14. Units

- Scalar/caesium total field: **nT**.
- Fluxgate/gradiometer and other magnetic gradient products: **nT/m**.
- Support/stability: dimensionless `[0–1]`.
- Interpolation distance: **m**.
- Measurement density: count/support density, not magnetic units.

The publication legend text can be overridden for presentation, but changing a label does not change the underlying raster unit.

## 15. Reproducibility

For a publication or archive, retain:

- original `RawData`;
- project metadata/config;
- processing command(s);
- quantitative reference rasters;
- correction/removed-component rasters;
- QC reports;
- figure JSON recipes;
- GCP/reprojection metadata where applicable.

---

**MagSurveyPy 1.0.1** — Archaeological Magnetometry Prospection Suite
Developed by **Alexandru Hegyi, PhD**
https://alexandruhegyi.com · alexandruhegyi@gmail.com · https://github.com/alexandruhegyi
