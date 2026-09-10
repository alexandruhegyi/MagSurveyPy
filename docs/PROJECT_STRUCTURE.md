# MagSurveyPy Project Structure

New MagSurveyPy v1.0.0 projects use acquisition-class names rather than manufacturer names.

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
