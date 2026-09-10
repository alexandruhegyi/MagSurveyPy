# MagSurveyPy v1.0.0

![MagSurveyPy](src/magsurveypy/assets/magsurveypy_logo.png)

**Archaeological Magnetometry Prospection Suite**  
Developed by **Alexandru Hegyi, PhD**  
Website: https://alexandruhegyi.com · Email: alexandruhegyi@gmail.com · GitHub: https://github.com/alexandruhegyi

MagSurveyPy is a project-based Python package and command-line application for archaeological magnetometry processing, quality control, analysis, visualization, GIS integration, cartographic export and local Web GIS. The public survey interface is organized around scientific acquisition classes rather than instrument manufacturers.

## Survey model

MagSurveyPy v1.0.0 uses two primary survey families:

```text
mspy survey multichannel ...
mspy survey grid --protocol total-field ...
mspy survey grid --protocol fluxgate ...
```

- **Multichannel**: multichannel magnetic acquisition, including supported native acquisition exports and normalized ASC/tabular data while retaining source, session, sensor and channel provenance where available.
- **Total field**: gridded scalar total magnetic field data in nT. A normal exported file may contain one final reading column and is processed directly.
- **Fluxgate**: gridded fluxgate magnetometry/gradiometry data, normally in nT/m.

File formats are adapters, not survey categories. Supported workflows include PRM as one multichannel input example, paired HDR/DAT as one grid-format example, and generic ASC/CSV/TXT/XYZ/DAT and quantitative GIS raster/vector formats where scientifically meaningful.

### Optional gradients from split-sensor total-field data

If a total-field file retains two simultaneous sensor channels, MagSurveyPy can create an **additional** vertical or horizontal gradient product without replacing the original total-field result:

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient vertical --sensor-separation 0.50

mspy survey grid --project Site --protocol total-field \
  --gradient horizontal --sensor-separation 0.50
```

For vertical geometry, the default paired-sensor convention is sensor 1/top and sensor 2/bottom, with `(top - bottom) / separation`. For horizontal geometry, sensor 1/left and sensor 2/right are used, with `(right - left) / separation`. Column names and sign convention can be specified explicitly. If a measured gradient column already exists, it can be used directly. **Sensor separation is never guessed.**

A file containing only one final reading column remains a standard total-field input; simply omit `--gradient`.

## Installation

### Recommended: pip

When MagSurveyPy is available from PyPI:

```bash
python -m pip install magsurveypy
```

For the current source checkout:

```bash
python -m pip install .
```

Installation creates the `mspy` command automatically through the package entry point:

```bash
mspy --version
mspy --help
mspy tools doctor
```

Upgrade later with:

```bash
python -m pip install --upgrade magsurveypy
```

Uninstall with:

```bash
python -m pip uninstall magsurveypy
```

This removes the installed Python package and the `mspy` entry point from the active environment. It does **not** remove MagSurveyPy projects, raw survey data, processed results, source folders or downloaded archives.

### Alternative: Conda environment

From the repository root:

```bash
conda env create -f environment.yml
conda activate magsurveypy
mspy --version
```

The supplied Conda environment installs the MagSurveyPy package itself, so the same `mspy` command is available; no manual launcher or shell alias is required.

See [INSTALL.md](INSTALL.md) for details.

## Project creation

Projects are stored by default under `~/MagSurveyPy_Projects/` and use generic acquisition folders:

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

Create a project according to its main acquisition class:

```bash
mspy project init Rupea --category multichannel
mspy project init Foeni --category total-field
mspy project init GradSite --category fluxgate
mspy project init MixedSite --category mixed
```

Import data into the corresponding generic branch:

```bash
mspy project import Rupea /path/to/data --type multichannel
mspy project import Foeni /path/to/data --type total-field
mspy project import GradSite /path/to/data --type fluxgate
```

`--mode link` can be used instead of copying files when appropriate.

## Typical workflows

### Multichannel magnetic acquisition

```bash
mspy project init Rupea --category multichannel
mspy project import Rupea /path/to/multichannel_export --type multichannel
mspy survey multichannel --project Rupea --format auto --workflow standard
mspy analyze survey --project Rupea
mspy process interpolate --project Rupea
# Explicit source files may also be written as:
mspy process interpolate --project Rupea --input ./points.asc --method archaeology
mspy figure single --project Rupea --from INTERPOLATED --display-range 15
```

Normalized ASC can be supplied directly where the existing multichannel importer supports it. Format-specific adapters can be selected explicitly when automatic detection is not suitable.

### Total-field grid

```bash
mspy project init Foeni --category total-field
mspy project import Foeni /path/to/total_field_data --type total-field
mspy survey grid --project Foeni --protocol total-field --workflow preservation
mspy analyze survey --project Foeni --from TOTAL_FIELD
```

A more archaeology-oriented processing example is:

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

The absolute/reference field is retained separately from derived archaeology-oriented products.

### Fluxgate / gradiometer grid

```bash
mspy project init GradSite --category fluxgate
mspy project import GradSite /path/to/grid_data --type fluxgate
mspy layout gui --project GradSite --protocol fluxgate
mspy layout validate --project GradSite --protocol fluxgate
mspy survey grid --project GradSite --protocol fluxgate --workflow archaeology
mspy analyze survey --project GradSite --from FLUXGATE
```

## Command groups

```text
project   create, import, configure and inspect projects
survey    initial acquisition-aware processing
layout    define and validate local-grid geometry
process   interpolation, cleaning, enhancement and derived products
filter    explicit observation/raster corrections
analyze   survey, line, sensor, raster, spectrum and stage QC
figure    scientific and publication figures
export    GIS/cartographic outputs and reprojection
web       interactive local Web GIS
gnss      GNSS/RINEX/PPK utilities
tools     diagnostics and generated help
guide     scientific workflow guides
help      detailed command help
```

Use `mspy --help`, `mspy project --help`, `mspy survey --help`, and `mspy survey grid --help` for built-in documentation.

## Reproducibility and data preservation

MagSurveyPy keeps original field files separate from derived products. Processing commands maintain project logs, and `--increment` can preserve an existing derived stage while creating a numbered output stage. Analysis commands create diagnostics without altering scientific data. Display-only controls such as brightness, contrast, gamma and saturation do not modify quantitative raster values.

## License and warranty

MagSurveyPy is distributed under the **BSD 3-Clause License**. The full legal terms are in [LICENSE](LICENSE).

The software is provided **“AS IS”**, without warranties of any kind. Users remain responsible for validating processing choices, coordinate systems, sensor geometry, derived gradients, quantitative outputs and archaeological interpretation for their own data and purpose.

## Citation

Citation metadata are supplied in [CITATION.cff](CITATION.cff). A persistent DOI will be added after the v1.0.0 release is archived.
