# Cleaning

Cleaning is consolidated under one public command:

```bash
mspy process clean --project Site --profile balanced
mspy process clean --project Site --profile strong
mspy process clean --project Site --profile very-strong
```

The cleaning stage combines robust background flattening, directional stripe suppression, edge-preserving denoising and restrained final smoothing. The source scientific raster is never overwritten. Always inspect the removed-component audit raster before interpretation.

For publication/display styling use `figure single` or `export map`; do not use plotting as a substitute for quantitative processing.
