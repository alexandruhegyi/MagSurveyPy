# Quick Start

## 1. Install

Recommended:

```bash
python -m pip install magsurveypy
```

From a source checkout before the PyPI release:

```bash
python -m pip install .
```

Verify:

```bash
mspy --version
mspy tools doctor
```

## 2. Create a project

Choose the scientific acquisition class:

```bash
mspy project init --project Site --category multichannel
mspy project init --project Site --category total-field
mspy project init --project Site --category fluxgate
```

## 3. Import data

```bash
mspy project import --project Site --input /path/to/data --type multichannel
mspy project import --project Site --input /path/to/data --type total-field
mspy project import --project Site --input /path/to/data --type fluxgate
```

## 4. Run the initial survey processing

Multichannel:

```bash
mspy survey multichannel --project Site --format auto --workflow standard
```

Total field:

```bash
mspy survey grid --project Site --protocol total-field --workflow preservation
```

Fluxgate/gradiometer:

```bash
mspy survey grid --project Site --protocol fluxgate --workflow archaeology
```

## 5. Optional gradient from split-sensor total-field data

Vertical:

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient vertical --sensor-separation 0.50
```

Horizontal:

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient horizontal --sensor-separation 0.50
```

Do not use a gradient option for ordinary one-reading total-field exports. MagSurveyPy does not invent a missing sensor separation.

## 6. Continue with derived products and QC

```bash
mspy analyze survey --project Site
mspy process interpolate --project Site
mspy figure single --project Site --from INTERPOLATED
mspy web --project Site
```
