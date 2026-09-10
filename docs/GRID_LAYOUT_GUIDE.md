# Total-Field Grid Layout Guide

Many archaeological scalar/caesium surveys consist of separate local grids whose internal X/Y coordinates restart in every file. MagSurveyPy uses an explicit layout CSV. Automatic layout inference is deliberately not part of the public workflow.

## Recommended project workflow

Import the local-grid files:

```bash
mspy project import Site /path/to/GridFolder --type total-field
```

Open the visual editor:

```bash
mspy layout gui --project Site --grid-width 40 --grid-height 40
```

The editor lets the user:

- choose the number of layout rows and columns;
- assign one DAT/STN file to each grid cell;
- choose 0, 90, 180, or 270 degree rotation per grid;
- preview the assembled network;
- save the project layout.

Project mode saves automatically to:

```text
Site/Layouts/grid_layout.csv
```

The CSV is explicit and reproducible:

```csv
file,offset_x,offset_y,rotation_deg
GRD1.dat,0,0,0
GRD2.dat,0,40,0
GRD3.dat,0,80,0
```

Validate before processing:

```bash
mspy layout validate --project Site
```

Validation checks file coverage, duplicate assignments, geometric overlap, and magnetic continuity along boundaries that the CSV says are physically adjacent.

Then run total-field processing:

```bash
mspy survey grid --protocol total-field --project Site --workflow preservation
```

MagSurveyPy automatically uses `Layouts/grid_layout.csv`; no CSV path is needed.

## Low-level path mode

The GUI and validator also accept explicit paths. Run:

```bash
mspy help layout gui
mspy help layout validate
```

for those advanced options.
