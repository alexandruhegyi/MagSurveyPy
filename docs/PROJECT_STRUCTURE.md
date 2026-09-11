# MagSurveyPy Project Structure

New MagSurveyPy v1.0.2 projects use acquisition-class names rather than manufacturer names.

```text
~/MagSurveyPy_Projects/
└── Site/
    ├── project.json
    ├── RawData/
    │   ├── Multichannel/
    │   ├── TotalField/
    │   ├── Fluxgate/
    │   ├── Generic/
    │   ├── GNSS/
    │   └── BaseStation/
    ├── Config/
    │   └── processing_defaults.json
    ├── Layouts/
    │   └── grid_layout.csv
    ├── Results/
    │   ├── MULTICHANNEL/
    │   ├── TOTAL_FIELD/
    │   ├── FLUXGATE/
    │   ├── GRADIENT_VERTICAL/
    │   ├── GRADIENT_HORIZONTAL/
    │   └── other derived stages as created
    ├── Reports/
    ├── Exports/
    ├── Logs/
    └── Temp/
```

Not every Results branch is created in every project. Gradient branches are produced only when explicitly requested from suitable split-sensor or measured-gradient data.

Raw files are kept separate from derived products. New projects never require a manufacturer-named raw-data folder. Older pre-release layouts may still be recognized internally so existing projects can be opened without migration.


## Native processing PNG structure

Automatic stage figures use the same subfolders wherever the product type applies:

```text
PNG/
  Comparison/   source/result/removed-component or equivalent stage comparisons
  Products/     individual quantitative/derived product previews
  QC/           quality-control and performance figures
  Diagnostics/  spectra, noise/support and specialist diagnostic figures
```

Automatic processing previews are intentionally undecorated. North arrows, scale bars, CRS labels and publication layout controls belong to `mspy figure` and `mspy export`.
