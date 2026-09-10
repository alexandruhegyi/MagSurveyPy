# MagSurveyPy v1.0.0 — Public release preparation

**MagSurveyPy v1.0.0 — Archaeological Magnetometry Prospection Suite**

This package is a publication-oriented revision of the existing v1.0.0 source tree. It does **not** change the numerical processing algorithms, scientific defaults, filter parameters, interpolation implementation, project routing, Web GIS behavior, or existing command semantics.

Public-facing terminology now describes the main acquisition classes as:

- multichannel magnetic acquisition;
- total-field grid acquisition;
- fluxgate magnetometry/gradiometry grid acquisition.

Older pre-release command and folder identifiers remain readable internally where needed for backward compatibility. The public v1.0.0 interface uses acquisition-class terminology. Normalized five-column ASC remains available as an instrument-independent point-data representation used by the gridding/interpolation engine.

A BSD 3-Clause license has been added. MagSurveyPy is distributed as-is, without warranty; users remain responsible for scientific validation and interpretation.


## Release-candidate CLI corrections

- `mspy process interpolate` accepts either a positional source path or `--input PATH`; both forms use the same interpolation engine.
- Public grouped commands normalize `--input PATH` where the existing engine uses positional source input, reducing avoidable CLI syntax failures without changing processing behavior.
- `mspy filter raster --stripe-auto --directional-notch` now calls the established spectral stripe-orientation diagnostic; the previous undefined function reference has been removed.
- Public `--help` output uses the `mspy` executable name and includes practical examples for each command category/subcategory.
- The public fluxgate layout template is named `FLUXGATE_LAYOUT_TEMPLATE.csv`.
