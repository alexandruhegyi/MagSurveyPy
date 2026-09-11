# MagSurveyPy v1.0.1 — Installation

MagSurveyPy supports Python 3.11 and newer. The installed command-line interface is `mspy`.

## Recommended installation: pip

### From PyPI

After the public PyPI release:

```bash
python -m pip install magsurveypy
```

Verify:

```bash
mspy --version
mspy --help
mspy tools doctor
```

### From a cloned or extracted source tree

From the directory containing `pyproject.toml`:

```bash
python -m pip install .
```

For development only:

```bash
python -m pip install -e .
```

To refresh an installed local checkout without reinstalling already-present dependencies:

```bash
python -m pip install --force-reinstall --no-deps .
```

The `[project.scripts]` entry in `pyproject.toml` creates `mspy` automatically. No shell launcher or manually created alias is required.

### Install directly from GitHub

After the public repository is ready:

```bash
python -m pip install git+https://github.com/alexandruhegyi/MagSurveyPy.git
```

### Upgrade

```bash
python -m pip install --upgrade magsurveypy
```

### Uninstall

```bash
python -m pip uninstall magsurveypy
```

If you installed into a virtual environment or Conda environment, activate that same environment before uninstalling. Uninstalling MagSurveyPy removes the installed package and `mspy` command from that environment only; it does not delete user projects, raw data, processed results, source folders or downloaded archives.

## Alternative installation: Conda environment

The supplied `environment.yml` is an alternative for users who prefer Conda/Miniforge. Run it from the MagSurveyPy source directory:

```bash
conda env create -f environment.yml
conda activate magsurveypy
mspy --version
mspy --help
```

The environment file installs both the scientific/GIS dependencies and the local MagSurveyPy package. Therefore the `mspy` command is created inside the Conda environment as well.

To remove the entire Conda environment:

```bash
conda deactivate
conda env remove -n magsurveypy
```

To keep the environment but uninstall only MagSurveyPy:

```bash
conda activate magsurveypy
python -m pip uninstall magsurveypy
```

## Project workspace

Projects are stored by default under:

```text
~/MagSurveyPy_Projects/
```

Set a custom workspace with `MAGSURVEYPY_WORKSPACE`.

Linux/macOS:

```bash
export MAGSURVEYPY_WORKSPACE=/data/MagSurveyPy_Projects
```

Windows PowerShell:

```powershell
$env:MAGSURVEYPY_WORKSPACE = "D:\MagSurveyPy_Projects"
```

## First project

Multichannel:

```bash
mspy project init --project Site --category multichannel
mspy project import --project Site --input /path/to/data --type multichannel
mspy survey multichannel --project Site --format auto --workflow standard
```

Total field:

```bash
mspy project init --project Site --category total-field
mspy project import --project Site --input /path/to/data --type total-field
mspy survey grid --project Site --protocol total-field --workflow preservation
```

Fluxgate/gradiometer:

```bash
mspy project init --project Site --category fluxgate
mspy project import --project Site --input /path/to/data --type fluxgate
mspy survey grid --project Site --protocol fluxgate --workflow archaeology
```

For split-sensor total-field data, optional gradient products can be added with `--gradient vertical` or `--gradient horizontal` and a known `--sensor-separation`.

## Linux Tk support

The local-grid layout editor uses Tk. Most Conda distributions and standard Python installers provide it. On a minimal Debian/Ubuntu system, if Tk is unavailable:

```bash
sudo apt install python3-tk
```

## Troubleshooting

Confirm which executable is active:

```bash
which mspy
mspy --version
python -m pip show magsurveypy
```

On Windows PowerShell use `Get-Command mspy` instead of `which mspy`.
