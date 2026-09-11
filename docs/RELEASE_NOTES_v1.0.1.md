# MagSurveyPy v1.0.1 — interface and figure consistency

MagSurveyPy v1.0.1 is a presentation and command-interface consistency update. It does not change the scientific processing algorithms, numerical defaults, interpolation mathematics, filtering mathematics, georeferencing, Web GIS quantitative behavior, or existing data adapters.

## Command-line consistency

- `--project NAME` is the canonical project spelling across the public CLI.
- Project-management commands continue to accept the historical positional project name for backward compatibility.
- `project import` accepts repeatable `--input PATH` while retaining positional source paths.
- `project georeference` accepts the same canonical `--project` / `--input` grammar.
- Help examples use the canonical spelling.

## Native processing figures

Automatic processing PNGs are organized under a common tree:

```text
PNG/
  Comparison/
  Products/
  QC/
  Diagnostics/
```

Automatic processing previews no longer receive publication cartography such as north arrows, scale bars, CRS badges, or footer prose. Those elements remain available in `mspy figure` and `mspy export`.

Colourbar tick density is now selected from the rendered bar length and formatted numerical labels. This is especially useful for absolute total-field values, where five-digit tick labels can otherwise overlap on compact horizontal bars.

The ENHANCED stage writes a standard Source / Enhanced / Removed component comparison in addition to individual product previews. Existing scientific rasters and reports are unchanged.

## Documentation and citation

- Refreshed the GitHub README with architecture, processing-domain, native PRM, and local GIS figures from the accompanying scientific manuscript.
- Added the Zenodo preprint DOI `10.5281/zenodo.22709406` to project metadata and `CITATION.cff` as the preferred scientific citation.
- Retained software-version citation guidance separately so users can cite the exact software release used in their work.
