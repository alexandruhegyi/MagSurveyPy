# Analysis and QC Guide

`analyze` is the non-destructive analytical layer of MagSurveyPy. It is designed to answer **what is in the survey and what processing problem is actually present** before additional filtering is chosen.

Analysis never modifies source observations or rasters.

## Comprehensive survey dashboard

```bash
mspy analyze survey --project Site
```

When points and a raster are available, the dashboard combines:

- spatial coverage / measurement geometry;
- magnetic value distribution;
- line/traverse baselines;
- robust line variability/noise;
- sensor/channel comparisons;
- spatial spectrum.

A JSON summary and CSV tables are written alongside the graph where applicable.

## Lines/traverses

```bash
mspy analyze lines --project Foeni --from TOTAL_FIELD
```

Use this before `--traverse-zero`, line detrending or aggressive destriping. Look for:

- alternating line offsets;
- drift within lines;
- one or a few anomalous traverses;
- changes in robust variability/noise between lines.

A real broad archaeological anomaly may also shift a line baseline, so line statistics must be interpreted with the map geometry.

## Sensors/channels

```bash
mspy analyze sensors --project Rupea --from NATIVE
```

Useful for multisensor systems to identify:

- persistent sensor offsets;
- one noisy channel;
- channel-dependent variance;
- sensor dropout or unusual sampling.

## Raster statistics

```bash
mspy analyze raster --project Rupea --from INTERPOLATED
```

Reports quantitative distribution metrics and unit-aware value statistics. This is useful for comparing processing stages without relying only on visual contrast.

## Spectrum and stripe diagnostics

```bash
mspy analyze spectrum --project Sanandrei --from INTERPOLATED
```

Outputs include a radial power spectrum and directional anisotropy/stripe diagnostics. Use this to decide whether a directional notch or wavelength-specific filter is justified.

A spectral peak is evidence of periodic structure, not proof that the structure is acquisition noise. Compare its direction/wavelength with known traversal geometry and archaeology.

## Compare stages

```bash
mspy analyze stages \
  --project Rupea \
  --stages NATIVE,INTERPOLATED,CLEAN
```

This provides a quantitative audit of how processing changed distribution and correlation. Pair it with:

```bash
mspy figure compare --project Rupea --stages NATIVE,INTERPOLATED,CLEAN
```

## Suggested publication/QC workflow

1. Run `analyze survey` on the earliest quantitative stage.
2. Save line/sensor/spectrum diagnostics that justify a correction.
3. Apply one scientifically motivated correction or stage.
4. Re-run relevant analysis.
5. Use `analyze stages` and `figure compare` to document the effect.
6. Keep removed-component products for transparency.
