# Workflow Cookbook

These examples use the public acquisition-class interface.

## Multichannel survey

```bash
mspy project init --project Rupea --category multichannel
mspy project import --project Rupea --input /path/to/acquisition_export --type multichannel
mspy survey multichannel --project Rupea --format auto --workflow standard
mspy analyze survey --project Rupea
mspy process interpolate --project Rupea
```

## Multichannel ploughed/noisy variants

```bash
mspy survey multichannel --project Site --format auto --workflow ploughed
```

```bash
mspy survey multichannel --project Site --format auto --workflow noisy
```

## Total-field preservation workflow

```bash
mspy project init --project Site --category total-field
mspy project import --project Site --input /path/to/data --type total-field
mspy survey grid --project Site --protocol total-field --workflow preservation
```

## Total-field archaeology workflow

```bash
mspy survey grid --project Site --protocol total-field \
  --traverse-zero median --deslope robust \
  --destripe protected --destripe-strength 1 \
  --high-pass 5 --archaeology-center robust \
  --cell-size 0.25 --statistic mean
```

## Optional vertical gradient from split total-field sensors

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient vertical --sensor-separation 0.50
```

## Optional horizontal gradient from split total-field sensors

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient horizontal --sensor-separation 0.50
```

These gradient commands retain `Results/TOTAL_FIELD` and add `Results/GRADIENT_VERTICAL` or `Results/GRADIENT_HORIZONTAL`.

## Fluxgate/gradiometer local grids

```bash
mspy project init --project GradSite --category fluxgate
mspy project import --project GradSite --input /path/to/grid_data --type fluxgate
mspy layout gui --project GradSite --protocol fluxgate
mspy layout validate --project GradSite --protocol fluxgate
mspy survey grid --project GradSite --protocol fluxgate --workflow archaeology
```

## Analysis and presentation

```bash
mspy analyze survey --project Site
mspy analyze spectrum --project Site --from INTERPOLATED
mspy figure single --project Site --from INTERPOLATED --display-range 15
mspy export map --project Site --from INTERPOLATED
mspy web --project Site
```
