# MagSurveyPy v1.0.2

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/src/magsurveypy/assets/magsurveypy_logo.png" alt="MagSurveyPy logo" width="720">
</p>

<p align="center">
  <strong>Archaeological Magnetometry Prospection Suite</strong><br>
  Open-source processing, analysis, quality control, GIS integration, cartography, and local GIS inspection for archaeological magnetometry.
</p>

<p align="center">
  <a href="https://pypi.org/project/magsurveypy/"><img src="https://img.shields.io/pypi/v/magsurveypy?label=PyPI&cacheSeconds=300" alt="PyPI version"></a>
  <a href="https://pypi.org/project/magsurveypy/"><img src="https://img.shields.io/pypi/pyversions/magsurveypy" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-BSD--3--Clause-blue" alt="BSD 3-Clause"></a>
  <a href="https://doi.org/10.5281/zenodo.22710282"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22710282.svg" alt="Software DOI"></a>
  <a href="https://doi.org/10.5281/zenodo.22709406"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22709406.svg" alt="Preprint DOI"></a>
</p>

**Developed by Alexandru Hegyi, PhD**<br>
Department of Geosciences, University of Oslo<br>
UiO: alexandru.hegyi@geo.uio.no · Personal: alexandruhegyi@gmail.com<br>
Website: https://alexandruhegyi.com · GitHub: https://github.com/alexandruhegyi

---

## Overview

MagSurveyPy is a project-based Python package and command-line application for archaeological magnetometry. It supports **multichannel magnetic acquisition**, **gridded total-field magnetometry**, and **fluxgate magnetometry/gradiometry** in a common workflow built around the `mspy` command.

The software combines:

- native and generic data import;
- acquisition-aware survey processing;
- interpolation with explicit spatial support;
- observation- and raster-domain filtering;
- line, traverse, grid, and background corrections;
- robust statistics, spectral analysis, and QC;
- enhancement and optional segmentation/vectorization;
- georeferencing and reprojection;
- quantitative GeoTIFF, ASCII-grid, CSV, and GIS export;
- scientific figures and cartographic output;
- a **local GIS interface** for interactive inspection, profiles, drawing, georeferencing, and current-view export;
- project history and incremented result branches for reproducibility.

Supported native readers are used where acquisition metadata are encoded in instrument files. Generic ASC, CSV, TXT, XYZ, DAT, raster, and GIS formats can be used when their coordinates and measurement fields are sufficiently defined.

---

## Software architecture

MagSurveyPy separates input decoding, positioning, project data, quantitative processing, analysis, and presentation. Raw inputs remain separate from derived products, while each processing stage can retain its own reports, diagnostics, previews, and comparisons.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/architecture_overview.svg" alt="MagSurveyPy software architecture" width="100%">
</p>

The project model is intentionally explicit:

```text
Project/
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

Automatic processing figures follow the same structure across result stages:

```text
PNG/
├── Comparison/
├── Products/
├── QC/
└── Diagnostics/
```

`Comparison/` contains the principal source/result comparison and, where relevant, a separately retained removed component. `Products/` contains clean raster previews, `QC/` contains quality-control figures, and `Diagnostics/` contains spectra and specialist diagnostic plots. Publication cartography remains under `mspy figure` and `mspy export`.

---

## Processing domains

Quantitative processing is separated from display-only operations. Acquisition decoding and positioning occur before observation-domain corrections; interpolation creates quantitative rasters with explicit support; raster filters create new quantitative branches; brightness, contrast, gamma, saturation, and display ranges remain presentation controls and do not rewrite raster values.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/processing_domains.svg" alt="MagSurveyPy processing domains" width="100%">
</p>

This distinction is important when evaluating filters. Where applicable, MagSurveyPy retains source, filtered, and removed-component products separately so that the effect of a processing choice can be inspected rather than inferred only from the appearance of the final map.

---

## Installation

### Recommended: pip

Install the published package with:

```bash
python -m pip install magsurveypy
```

Upgrade with:

```bash
python -m pip install --upgrade magsurveypy
```

Verify the installation:

```bash
mspy --version
mspy --help
mspy tools doctor
```

Install from a source checkout with:

```bash
python -m pip install .
```

Uninstall with:

```bash
python -m pip uninstall magsurveypy
```

Uninstalling removes the installed Python package and the `mspy` command from the active environment. It does **not** remove MagSurveyPy projects, raw data, processed results, source folders, or downloaded archives.

### Alternative: Conda environment

From the repository root:

```bash
conda env create -f environment.yml
conda activate magsurveypy
mspy --version
```

The supplied environment installs MagSurveyPy itself, so `mspy` is created automatically.

See [INSTALL.md](INSTALL.md) and [docs/INSTALL.md](docs/INSTALL.md) for details.

---

## Quick start

The canonical public syntax uses the same option names across the application:

```text
--project    working project
--input      explicit external input, where required
--from       existing result stage
--output     explicit output override
--increment  preserve an existing result and create a numbered branch
```

A compact multichannel workflow is:

```bash
mspy project init --project Site --category multichannel
mspy project import --project Site --input /path/to/data --type multichannel
mspy survey multichannel --project Site --format auto --workflow standard
mspy analyze survey --project Site
mspy process interpolate --project Site --method archaeology
mspy web --project Site
```

Historical positional project/input forms remain accepted for compatibility, but new documentation uses the explicit option-based syntax.

---

## Survey workflows

### Multichannel magnetic acquisition

```bash
mspy project init --project Site --category multichannel
mspy project import --project Site --input /path/to/multichannel_data --type multichannel
mspy survey multichannel --project Site --format auto --workflow standard
mspy analyze survey --project Site
mspy process interpolate --project Site --method archaeology
```

Normalized ASC can also be supplied directly where supported. Source/session/sensor/channel provenance is retained where the input format provides it.

### Direct supported SENSYS PRM workflow

For implemented SENSYS PRM structures, MagSurveyPy can decode native magnetic words together with embedded GPS fixes and stored probe geometry. This allows georeferenced observations to be reconstructed directly from the acquisition data without a mandatory intermediate conversion through DLMGPS or MAGNETO.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/native_prm_workflow.svg" alt="Direct native PRM workflow" width="95%">
</p>

Native compatibility is format-specific; supported PRM structures should not be interpreted as universal compatibility with every historic or future PRM variant.

### Gridded total-field magnetometry

```bash
mspy project init --project Site --category total-field
mspy project import --project Site --input /path/to/total_field_data --type total-field
mspy survey grid --project Site --protocol total-field --workflow preservation
mspy analyze survey --project Site --from TOTAL_FIELD
```

A more archaeology-oriented processing example is:

```bash
mspy survey grid --project Site --protocol total-field \
  --traverse-zero median \
  --deslope robust \
  --destripe protected \
  --destripe-strength 1 \
  --high-pass 5 \
  --archaeology-center median \
  --cell-size 0.25 \
  --statistic mean
```

The absolute/reference field remains separate from derived archaeology-oriented products.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/total_field_processing.png" alt="Total-field interpolation and processing workflow" width="100%">
</p>

<p align="center"><em>
Example total-field workflow showing measured-cell support, interpolation, and derived processing products. The support information makes the distinction between measured and interpolated areas explicit.
</em></p>

### Fluxgate magnetometry / gradiometry

```bash
mspy project init --project Site --category fluxgate
mspy project import --project Site --input /path/to/grid_data --type fluxgate
mspy layout gui --project Site --protocol fluxgate
mspy layout validate --project Site --protocol fluxgate
mspy survey grid --project Site --protocol fluxgate --workflow archaeology
mspy analyze survey --project Site --from FLUXGATE
```

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/fluxgate_cleaning_public.png" alt="Fluxgate processing comparison" width="100%">
</p>

<p align="center"><em>
Example multichannel fluxgate/gradiometer processing comparison. The reference raster is retained so that alternative processing branches can be evaluated against the same quantitative input.
</em></p>

### Optional paired-sensor gradients

If a total-field file retains paired sensor channels, an additional vertical or horizontal gradient can be derived when the physical sensor geometry is known. Existing measured-gradient columns can also be used directly. Sensor separation is never silently inferred.

```bash
mspy survey grid --project Site --protocol total-field \
  --gradient vertical --sensor-separation 0.50
```

Gradient derivation is an optional secondary product; ordinary one-column total-field data remain normal total-field inputs.

---

## Interpolation, filtering, QC, and segmentation

MagSurveyPy provides several interpolation and processing branches, including:

- measured-cell aggregation;
- linear TIN interpolation;
- inverse-distance weighting;
- local kriging;
- nearest-neighbour and bounded cubic alternatives;
- support masks and preserved NoData gaps;
- robust despiking;
- traverse and line levelling;
- Gaussian and median filtering;
- spatial high-pass/low-pass filtering;
- Fourier-domain filters and directional diagnostics;
- plane removal and upward continuation;
- survey, line, sensor, raster, and spectral QC;
- optional segmentation and candidate vectorization as interpretive support.

Segmentation produces auxiliary candidate objects and does not replace the quantitative magnetic raster or constitute automatic archaeological interpretation.

### Inspecting filtering results

Where appropriate, MagSurveyPy retains source, filtered, and removed-component products separately. This makes it possible to evaluate what a filter removed rather than judging the processing only from the final map.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/challenging_data_filtering.png" alt="Challenging magnetic raster processing example" width="100%">
</p>

<p align="center"><em>
Example processing of a challenging magnetic raster. Source and derived branches are retained separately so that the effect of cleaning and filtering can be inspected directly.
</em></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/multichannel_filter_removed_component.png" alt="Multichannel filtering and removed-component audit" width="100%">
</p>

<p align="center"><em>
Multichannel filtering example showing the source raster, retained filtered component, and removed component. The removed component provides a direct audit of the structures suppressed by the selected filter.
</em></p>

---

## Local GIS interface

Launch the local GIS interface with:

```bash
mspy web --project Site
```

It provides project-aware raster display, basemaps, statistics, profiles, drawing tools, georeferencing, layer controls, and export of the current map view. Display adjustments such as brightness, contrast, gamma, saturation, opacity, and manual display limits do not alter the stored quantitative raster.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexandruhegyi/MagSurveyPy/v1.0.2/docs/assets/local_gis_public.png" alt="MagSurveyPy local GIS interface" width="100%">
</p>

The local GIS is intended for rapid project-linked inspection and spatial work; it does not attempt to replace a full desktop GIS.

---

## Command groups

| Group | Purpose |
|---|---|
| `project` | create, import, configure, inspect, and track projects |
| `survey` | acquisition-aware multichannel and grid processing |
| `layout` | define and validate local-grid geometry |
| `process` | interpolation, cleaning, enhancement, segmentation, thinning |
| `filter` | observation- and raster-domain corrections |
| `analyze` | survey, line, sensor, raster, spectrum, and stage QC |
| `figure` | scientific and publication figures |
| `export` | GIS/cartographic output, reprojection, contours, bundles |
| `web` | local GIS interface |
| `gnss` | GNSS/RINEX/PPK utilities |
| `tools` | diagnostics and generated help |
| `guide` | scientific workflow guides |
| `help` | detailed command help |

Start with:

```bash
mspy --help
mspy project --help
mspy survey --help
mspy survey grid --help
mspy guide projects
mspy guide installation
```

The detailed documentation is under [`docs/`](docs/), including workflow, filtering, interpolation, total-field, fluxgate, PRM, georeferencing, export, QC, and local GIS guides.

---

## Reproducibility and data preservation

MagSurveyPy keeps field inputs separate from derived products. Processing commands maintain project histories, and `--increment` can preserve an existing stage while creating a numbered alternative. Analysis commands create diagnostics without modifying scientific data.

The project structure therefore preserves the distinction between:

1. source/acquisition data;
2. normalized observations;
3. quantitative processing stages;
4. QC and diagnostic products;
5. publication/cartographic outputs;
6. display-only operations.

---

## Scientific description and citation

A detailed description of the architecture, numerical processing, native PRM workflow, GIS handling, QC, and reproducibility model is available as a Zenodo preprint:

> **Hegyi, A. (2026). _MagSurveyPy: An Open-Source Framework for Archaeological Magnetometry Processing and Spatial Analysis_ (Version 1). Zenodo.**<br>
> https://doi.org/10.5281/zenodo.22709406

The current version-specific software archive is:

> **Hegyi, A. (2026). _MagSurveyPy: Archaeological Magnetometry Prospection Suite_ (Version 1.0.1) [Computer software]. Zenodo.**<br>
> https://doi.org/10.5281/zenodo.22710282

For research use, please cite the **scientific description** and the **specific software version used**. The `CITATION.cff` file contains the version-specific software DOI and identifies the preprint as the preferred scientific citation.

See [CITATION.cff](CITATION.cff).

---

## v1.0.2 documentation and metadata maintenance

Version 1.0.2 is a documentation and metadata maintenance release. It does not change the scientific processing algorithms, numerical defaults, interpolation mathematics, filtering mathematics, georeferencing, native data decoding, or quantitative GIS behaviour established in v1.0.1.

The release updates the project README and scientific workflow illustrations, uses PyPI-compatible absolute image references, refreshes package and citation metadata, and improves consistency between the GitHub, PyPI, Zenodo, and preprint presentation.

See [docs/RELEASE_NOTES_v1.0.2.md](docs/RELEASE_NOTES_v1.0.2.md).

## v1.0.1 consistency update

Version 1.0.1 is a consistency-focused release. It does not intentionally change the established scientific processing algorithms. The main changes are:

- uniform `--project`, `--input`, `--from`, `--output`, and `--increment` conventions;
- compatibility with historical positional forms;
- consistent `PNG/Comparison`, `PNG/Products`, `PNG/QC`, and `PNG/Diagnostics` output organization;
- common automatic raster-preview and comparison styling;
- adaptive colorbar tick density to avoid overlapping labels, including large absolute total-field values;
- separation of routine processing previews from explicit publication/cartographic decoration;
- retained removed-component products where appropriate for filtering audits;
- updated documentation and citation metadata.

See [docs/RELEASE_NOTES_v1.0.1.md](docs/RELEASE_NOTES_v1.0.1.md).

---

## License and warranty

MagSurveyPy is distributed under the **BSD 3-Clause License**. See [LICENSE](LICENSE).

The software is provided **“AS IS”**, without warranties of any kind. Users remain responsible for validating processing choices, coordinate systems, sensor geometry, quantitative outputs, and archaeological interpretation for their own data and purpose.
