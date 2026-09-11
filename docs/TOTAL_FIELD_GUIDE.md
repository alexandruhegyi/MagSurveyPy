# Total-Field Grid Guide

Total-field projects contain scalar total magnetic field measurements, normally in nT. The primary public command is:

```bash
mspy survey grid --project Site --protocol total-field
```

## Standard one-reading exports

Most exported DAT/CSV/TXT files contain a coordinate pair and one final magnetic reading column. Process these normally:

```bash
mspy project init --project Foeni --category total-field
mspy project import --project Foeni --input /path/to/data --type total-field
mspy survey grid --project Foeni --protocol total-field --workflow preservation
```

No sensor geometry or gradient option is required.

The reference/absolute field is retained separately from derived archaeology-oriented processing.

## Archaeology-oriented processing

Example:

```bash
mspy survey grid --project Foeni --protocol total-field \
  --traverse-zero median \
  --deslope robust \
  --destripe protected \
  --destripe-strength 1 \
  --high-pass 5 \
  --archaeology-center median \
  --cell-size 0.25 \
  --statistic mean
```

Use processing options according to the acquisition geometry, noise sources and archaeological objective. Preserve the reference result for comparison.

## Split-sensor files and optional gradients

Some total-field files retain both simultaneous sensor measurements rather than only the combined/final reading. In that case MagSurveyPy can create an additional gradient branch while still running and retaining the normal total-field workflow.

### Vertical gradient

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient vertical \
  --sensor-separation 0.50
```

Default paired-sensor geometry:

```text
sensor 1 = top
sensor 2 = bottom / ground-near
vertical gradient = (top - bottom) / separation
```

Override unusual column names with `--top-column`, `--bottom-column`, `--sensor1-column` or `--sensor2-column`. The sign convention can be changed explicitly with `--gradient-sign`.

### Horizontal gradient

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient horizontal \
  --sensor-separation 0.50
```

Default paired-sensor geometry:

```text
sensor 1 = left
sensor 2 = right
horizontal gradient = (right - left) / separation
```

Override column names with `--left-column` and `--right-column` when needed.

### Existing measured gradient

If the file already includes a recognized `vertical_gradient` or `horizontal_gradient` column, MagSurveyPy can use it directly. An explicitly named column can be selected with `--gradient-column`.

### Safety rule

MagSurveyPy never guesses a missing physical sensor separation. If a requested gradient must be derived from two magnetic channels and the separation cannot be read from the file or supplied explicitly, the gradient operation stops with an error. The original total-field data remain the primary product.
