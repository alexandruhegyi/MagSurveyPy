# MagSurveyPy v1.0.3 — terminal compatibility and installation update

MagSurveyPy v1.0.3 is a small cross-platform compatibility and documentation patch release.

There are no intended changes to scientific processing algorithms, numerical defaults, interpolation mathematics, filtering mathematics, georeferencing, native data decoding, or quantitative GIS behaviour relative to v1.0.2.

Changes in v1.0.3:

- terminal banner uses the terminal's default foreground colour instead of forcing black text;
- banner visibility is improved on both dark and light terminal themes;
- Windows installation guidance recommends an isolated Miniconda or Anaconda environment followed by installation from PyPI with `pip`;
- macOS installation guidance uses the same Conda-environment plus PyPI workflow;
- direct `pip` installation remains supported for suitable Python environments.

MagSurveyPy is installed from PyPI. Conda is used only for environment management; MagSurveyPy is not currently distributed through a Conda channel.

Scientific description:

Hegyi, A. (2026). *MagSurveyPy: An Open-Source Framework for Archaeological Magnetometry Processing and Spatial Analysis* (Version 1). Zenodo.

https://doi.org/10.5281/zenodo.22709406

The archived v1.0.1 software record remains scientifically representative of the processing functionality:

https://doi.org/10.5281/zenodo.22710282
