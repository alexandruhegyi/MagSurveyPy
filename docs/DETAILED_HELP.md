# Detailed Help

The executable help is the authoritative option reference for MagSurveyPy 1.0.3.

```bash
mspy --help
mspy <group> --help
mspy help <group> <command>
```

Examples:

```bash
mspy help survey grid
mspy survey grid --help
mspy help filter raster
mspy help analyze spectrum
mspy help figure build
```

Generate a complete snapshot:

```bash
mspy tools help-all > HELP_ALL.txt
```

For practical workflows rather than option-by-option syntax, read `WORKFLOW_COOKBOOK.md`.

Every public category and subcommand help page includes at least one practical command example. Public usage lines use the installed `mspy` executable name.
