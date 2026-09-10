# Fluxgate / Gradiometer Grid Guide

MagSurveyPy treats fluxgate magnetometry/gradiometry as a scientific grid acquisition class rather than as a manufacturer-specific workflow. Products are normally expressed in nT/m when the source contains a magnetic gradient.

## Project setup

```bash
mspy project init GradSite --category fluxgate
mspy project import GradSite /path/to/grid_data --type fluxgate
```

Input is stored in:

```text
RawData/Fluxgate/
```

## Layout

For surveys acquired as multiple local grids:

```bash
mspy layout gui --project GradSite --protocol fluxgate
mspy layout validate --project GradSite --protocol fluxgate
```

## Process

```bash
mspy survey grid --project GradSite --protocol fluxgate --workflow archaeology
```

Primary output is written to:

```text
Results/FLUXGATE/
```

Supported format adapters may use companion metadata/data files to recover local-grid geometry and acquisition metadata. Such file names and structures are input formats only; they do not change the project category.

## Scientific note

Do not treat gradient values in nT/m as scalar total-field values in nT. Broad background-removal choices may also differ between an already differenced gradiometer product and a scalar total-field survey. Inspect the reference product and QC before applying optional filtering.
