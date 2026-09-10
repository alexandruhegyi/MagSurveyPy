# Filters Guide — Where a Correction Belongs

Filtering in MagSurveyPy is intentionally separated by **data level**. This prevents a display operation, an instrument correction and a quantitative spatial filter from being confused with each other.

## 1. `survey`: acquisition/instrument-aware corrections

Use `survey` when the correction depends on how the instrument acquired the data: sensor geometry, traverses, grids, protected destriping, total-field reference preservation, companion fluxgate-grid metadata, sensor levelling, crossover geometry, etc.

Examples:

```bash
mspy survey grid --protocol total-field --project Site --traverse-zero median --destripe protected
mspy survey grid --protocol fluxgate --project GradSite --grid-level network
```

These operations know the instrument branch and its units.

## 2. `filter observations`: normalized points before gridding

Use when you have normalized observations and want an explicit point/line correction independent of the proprietary source format.

```bash
mspy filter observations \
  --project Foeni --from TOTAL_FIELD \
  --despike-sigma 6 \
  --line-detrend linear \
  --line-zero robust \
  --center median
```

Important options:

- `--despike-sigma`: MAD-based isolated point rejection; 5–8 is a conservative QC range.
- `--line-zero mean|median|robust`: subtract one baseline per traverse.
- `--line-detrend linear`: remove linear along-line drift.
- `--center mean|median|robust`: subtract one final constant from all filtered observations.

Outputs contain original value, filtered value, removed component and despike flags. Source observations are never overwritten.

### Archaeological caution

Per-line zeroing can suppress a real broad anomaly when it occupies a large fraction of a traverse. Median/robust modes are safer than arithmetic mean, but no method is universally appropriate. Analyze line behavior before and after correction.

## 3. `filter raster`: quantitative spatial filtering after gridding

```bash
mspy filter raster \
  --project Rupea --from INTERPOLATED \
  --high-pass 8
```

Available filter families:

- Gaussian low-pass: suppress high-frequency noise, but can blur compact archaeology.
- Gaussian high-pass: remove broad regional/geological background, but can suppress broad archaeological structures.
- Median low/high-pass: robust to isolated extremes but can alter anomaly morphology.
- FFT Butterworth/Gaussian filters: explicit wavelength-band control.
- Upward continuation: physically meaningful potential-field smoothing.
- Plane removal: broad linear regional trend removal.
- Directional notch: suppress repetitive stripes at a diagnosed orientation.

For directional striping:

```bash
mspy analyze spectrum --project Site --from INTERPOLATED
mspy filter raster \
  --project Site --from INTERPOLATED \
  --directional-notch --stripe-auto --stripe-strength 0.6
```

An explicit raster path can also be supplied with `--input`:

```bash
mspy filter raster --input ./grid.tif -o FILTERED --high-pass 8
```

Every raster-filter run writes the final filtered raster **and the total removed component**. Interpret both.

## 4. `figure`/`export`: visualization only

A display range such as ±10 or ±20 does not alter data:

```bash
mspy figure single --project Foeni --from TOTAL_FIELD --display-range 20
```

Do not use display clipping as a substitute for quantitative processing.

## Recommended decision sequence

```text
analyze → identify a specific problem → choose the correct data level → filter/correct → inspect removed component → analyze again
```

If you cannot state what physical/acquisition problem a filter is intended to address, do not apply it by default.
