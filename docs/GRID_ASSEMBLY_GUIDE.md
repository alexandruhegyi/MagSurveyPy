# Grid Assembly Guide

For scalar/total-field local grids, assembly is project based and explicit. Import the field grids, create the layout visually, validate it and process the survey:

```bash
mspy project init --project Site --category total-field
mspy project import --project Site --input /path/to/GridFolder --type total-field
mspy layout gui --project Site --grid-width 40 --grid-height 40
mspy layout validate --project Site
mspy survey grid --protocol total-field --project Site --workflow preservation
```

The GUI saves `Layouts/grid_layout.csv`; the survey command uses it automatically. Automatic layout guessing is not part of the public interface.

For generic non-total-field imports use `survey generic --project Site`; inspect `mspy help survey generic` for the detailed input options.
