# Software Architecture and Public API

MagSurveyPy 1.0.1 is designed as a scientific library/application rather than a collection of unrelated scripts.

## Public command architecture

```text
Project/data provenance
        project
           ↓
Instrument-aware acquisition processing
        survey + layout + gnss
           ↓
Core quantitative derived stages
        process
           ↓
Optional explicit corrections
        filter
           ↓
Non-destructive QC/statistics
        analyze
           ↓
Publication composition       GIS/cartography
        figure                 export / web
```

Each public group has one scientific responsibility. Old standalone public aliases are intentionally not part of the supported 1.0.1 interface.

## Source organization

`magsurveypy.py` remains the executable orchestration layer and contains the mature instrument-processing engines retained from development.

New reusable analytical modules are separated under `magsurveypy_lib/`:

```text
magsurveypy_lib/
  analysis.py       raster/point statistics, line/sensor QC, spectra, dashboards
  point_filters.py  auditable normalized-observation filters
  figures.py        recipe-driven publication figure construction
```

This separation makes the high-level analytical code testable and reusable without duplicating the mature field-data processing engines.

## Stable public API vs internal implementation

Only commands shown by:

```bash
mspy --help
```

are considered the supported public CLI. Internal engine functions and adapters are implementation details and may be reorganized without changing the scientific command surface.

This is deliberate: reproducible papers and workflows should cite/use stable grouped commands, not internal function names.

## Data preservation

- `RawData/` is treated as source/provenance data.
- Instrument-aware corrected/reference products are preserved before archaeology-only residual transforms.
- Optional filters create new derived products.
- Analysis creates reports only.
- Figures and WebGIS styles do not rewrite quantitative rasters.

## Unit model

- scalar/total-field magnetometry: **nT**;
- Fluxgate/gradiometer grid products: **nT/m**;
- figure/export labels infer units from product metadata/path rather than forcing one global label.

## Why filters are split

A per-traverse zeroing correction and a Gaussian high-pass are scientifically different operations. One acts on acquisition observations and one acts on a spatial field. Keeping them in separate commands prevents order-of-operation ambiguity and makes methods sections easier to reproduce.

## Figure recipes

Publication figures are represented by editable JSON recipes rather than a large number of hard-coded panel combinations. This keeps the number of commands small while allowing many scientifically useful layouts.

## Reproducibility

A publishable workflow should retain:

- project configuration;
- raw-data provenance;
- exact CLI commands;
- relevant analysis JSON/CSV;
- removed-component products for optional filters;
- figure JSON recipe;
- MagSurveyPy version and dependency/environment information.

## Georeferencing layer

`magsurveypy_lib/georef.py` is the reusable GCP georeferencing engine. The public interfaces are:

- Web GIS **Georef** workspace.
- `project georeference` CLI.

The engine fits a transparent least-squares affine transform from 3+ image/target control points, reports residual QC, copies the quantitative magnetic array unchanged into a new GeoTIFF, and writes a GCP CSV plus JSON recipe. Subsequent CRS warping is deliberately delegated to `export reproject` so georeferencing and resampling remain separate auditable operations.
