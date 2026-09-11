# Command history, reproducibility and numbered outputs

MagSurveyPy 1.0.3 records project-scoped commands automatically so processing decisions can be traced and repeated later.

## Project Logs folder

Every project contains:

```text
PROJECT/
└── Logs/
    ├── commands.log
    ├── project.log
    ├── survey.log
    ├── layout.log
    ├── process.log
    ├── filter.log
    ├── analyze.log
    ├── figure.log
    ├── export.log
    ├── web.log
    └── command_status.tsv
```

`commands.log` is the chronological master history. Category files contain only commands from that command group. Each line contains a local timestamp and the exact reusable `mspy ...` command.

Example:

```text
[2026-09-10T01:29:00+02:00] mspy layout gui --project RUPEA2017CS --protocol total-field
```

`command_status.tsv` additionally records command category, completion status and duration. Logging is intentionally non-fatal: inability to write a log must never make a scientific processing command fail.

Existing projects do not need migration. `Logs/` is created automatically the next time a project-scoped command runs.

## Inspect command history in the terminal

Master history:

```bash
mspy project history --project RUPEA2017CS --tail 30
```

Only layout commands:

```bash
mspy project history --project RUPEA2017CS --category layout --tail 20
```

Other useful categories include `survey`, `process`, `filter`, `analyze`, `figure`, `export`, `web` and `project`.

## Preserve an existing output with `--increment`

MagSurveyPy keeps its existing overwrite behavior unless requested otherwise. Add:

```bash
--increment
```

or the equivalent alias:

```bash
--new-output
```

to create a numbered result when the normal target already exists.

Examples:

```bash
mspy process interpolate --project Rupea --increment
```

If `Results/INTERPOLATED` already exists, the new run is written to:

```text
Results/INTERPOLATED_1
```

The next run becomes `_2`, and so on.

For figures:

```bash
mspy figure single --project Rupea --from INTERPOLATED --increment
```

produces, as required:

```text
Rupea_INTERPOLATED_figure.png
Rupea_INTERPOLATED_figure_1.png
Rupea_INTERPOLATED_figure_2.png
```

The same policy is available for map exports, comparison figures, figure recipes/builds, filters, reprojection, contours and dissemination bundles.

## Standard-deviation visualization stretch

For maps and figures, a display can be clipped to a statistical range without modifying the quantitative raster:

```bash
mspy export map --project Rupea --from INTERPOLATED --display-std 2
```

`--display-std 2` means:

```text
mean - 2 standard deviations  ...  mean + 2 standard deviations
```

This is a visualization rule only. It does not rewrite or clip the GeoTIFF values.

The three display-limit modes are mutually exclusive:

```text
--display-min / --display-max   exact physical limits
--display-range N              median-centred ±N
--display-std N                mean-centred ±N standard deviations
```

The standard-deviation mode matches the corresponding stretch concept in the Web GIS.
