# Troubleshooting

## Check the environment

```bash
mspy tools doctor
```

## See all current commands

```bash
mspy tools help-all
```

## Interpolation fills a real acquisition gap

Default Version 1.0.1 behavior preserves large gaps. Confirm the report says `Gap policy: auto`. To be more conservative:

```bash
mspy process interpolate --project Site --max-gap 0.75
```

Inspect `Results/INTERPOLATED/GeoTIFF/*_preserved_gaps.tif`.

## Strong dipoles look clipped

For a full-amplitude comparison:

```bash
mspy process interpolate --project Site --clip off
```

## Satellite/OSM basemap is unavailable

Install the optional map dependency and ensure internet access:

```bash
conda install -c conda-forge contextily
```

## Cleaning removes archaeology

Use a less aggressive profile and inspect the removed-total raster:

```bash
mspy process clean --project Site --profile balanced
```
