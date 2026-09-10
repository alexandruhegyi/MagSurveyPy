# Project Management Guide

MagSurveyPy projects separate immutable/raw inputs from processing products, reports, exports and command history. The default workspace is `~/MagSurveyPy_Projects`.

## Survey categories

Choose the category that best describes the primary acquisition:

| Category | Use for | Main raw folder | Primary survey command |
|---|---|---|---|
| `multichannel` | Multiple simultaneous magnetic sensors/channels or acquisition sessions | `RawData/Multichannel` | `mspy survey multichannel` |
| `total-field` | Scalar total magnetic field grids, normally nT | `RawData/TotalField` | `mspy survey grid --protocol total-field` |
| `fluxgate` | Fluxgate/gradiometer grid products, normally nT/m | `RawData/Fluxgate` | `mspy survey grid --protocol fluxgate` |
| `mixed` | Projects combining more than one acquisition class | the relevant branches | choose the relevant survey command |

The category is project metadata; it does not prevent you from importing another supported data class later.

## Create a project

### Multichannel

```bash
mspy project init Rupea --category multichannel
```

Use this when measurements contain multiple sensors/channels, repeated acquisition sessions, or a multichannel acquisition export. Supported formats are adapters; the project is not tied to a manufacturer.

### Total field

```bash
mspy project init Foeni --category total-field
```

Use this for scalar total magnetic field measurements. A common exported DAT/CSV contains coordinates plus one final reading column. Such files are processed normally and do not require sensor geometry.

If the file retains two sensor readings, the same total-field workflow can optionally derive a vertical or horizontal gradient:

```bash
mspy survey grid --project Foeni --protocol total-field \
  --gradient vertical --sensor-separation 0.50
```

or:

```bash
mspy survey grid --project Foeni --protocol total-field \
  --gradient horizontal --sensor-separation 0.50
```

### Fluxgate / gradiometer

```bash
mspy project init GradSite --category fluxgate
```

Use this for gridded fluxgate magnetometry/gradiometry. Paired metadata/data files are supported where implemented, but the project category remains `fluxgate` regardless of manufacturer.

### Mixed project

```bash
mspy project init Site --category mixed
```

Use this when the same archaeological project contains multiple acquisition classes.

Optional metadata can be supplied during creation:

```bash
mspy project init Site --category total-field --crs EPSG:32635 --notes "Survey area 2"
```

## Generic folder structure

```text
Site/
├── project.json
├── RawData/
│   ├── Multichannel/
│   ├── TotalField/
│   ├── Fluxgate/
│   ├── Generic/
│   ├── GNSS/
│   └── BaseStation/
├── Config/
├── Layouts/
├── Results/
├── Reports/
├── Exports/
├── Logs/
└── Temp/
```

New projects use only these generic names. Older pre-release project trees remain readable for compatibility, but new data should be placed/imported into the generic folders.

## Import raw data

Copy files into the project:

```bash
mspy project import Site /path/to/data --type multichannel
mspy project import Site /path/to/data --type total-field
mspy project import Site /path/to/data --type fluxgate
```

Link instead of copying:

```bash
mspy project import Site /path/to/data --type total-field --mode link
```

Other supported branches are `generic`, `gnss` and `base-station`.

When the source is a directory, files are imported while preserving useful relative subfolders; the source directory itself is not unnecessarily duplicated as a wrapper level.

## Configure defaults

Show defaults:

```bash
mspy project config Site
```

Set common values:

```bash
mspy project config Site --cell-size 0.25 --fill-distance 0.50 --statistic median --cores 8
```

## Inspect the project

```bash
mspy project list
mspy project status Site
mspy project tree Site
mspy project path Site
```

## Local-grid layout

For total-field grids:

```bash
mspy layout gui --project Site --protocol total-field
mspy layout validate --project Site --protocol total-field
```

For fluxgate/gradiometer grids:

```bash
mspy layout gui --project Site --protocol fluxgate
mspy layout validate --project Site --protocol fluxgate
```

Layouts are saved under `Layouts/` and can be reused by survey processing.
