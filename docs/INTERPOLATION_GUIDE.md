# Archaeological Interpolation

## Recommended command

```bash
mspy process interpolate --project Site
```

When an explicit normalized observation file is preferred, both equivalent forms are accepted:

```bash
mspy process interpolate ./points.asc --project Site --method archaeology
mspy process interpolate --project Site --input ./points.asc --method archaeology
```

MagSurveyPy reads the authoritative ASC, forms robust measured-cell medians and interpolates only where there is suitable measured support.

## Gaps

The default is `--gap-policy auto`.

- small interruptions in otherwise supported measurements are filled;
- large acquisition holes remain NoData;
- the same support mask is used by archaeology/TIN, IDW, kriging, cubic and nearest;
- `*_preserved_gaps.tif` shows where interpolation was deliberately refused.

At 0.25 m cells the automatic maximum small-gap width is 1.0 m. The automatic value scales with cell size rather than using a sensor-specific spacing.

Explicit examples:

```bash
mspy process interpolate --project Site --max-gap 0.75
mspy process interpolate --project Site --max-gap 1.50
mspy process interpolate --project Site --gap-policy bridge
```

`bridge` should be used only when a continuous surface across enclosed acquisition holes is scientifically intended.

## Methods

```text
archaeology  default linear TIN within accepted support + positive IDW only for numerical/edge fallback
tin          linear Delaunay/TIN
idw          positive-weight inverse distance
kriging      local ordinary kriging
cubic        bounded Clough-Tocher cubic
nearest      nearest measured-cell diagnostic
```

## Clipping

Clipping affects only the derived interpolation input, never ASC/NATIVE values. For direct comparison of strong dipoles use:

```bash
mspy process interpolate --project Site --clip off
```
