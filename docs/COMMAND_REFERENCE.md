# Command Reference — Public v1.0.0 Interface

The installed executable is `mspy`.

## Project

```bash
mspy project init PROJECT --category multichannel|total-field|fluxgate|mixed
mspy project import PROJECT SOURCE --type multichannel|total-field|fluxgate|generic|gnss|base-station
mspy project config PROJECT [options]
mspy project status PROJECT
mspy project tree PROJECT
mspy project path PROJECT
mspy project history PROJECT
```

Examples:

```bash
mspy project init Rupea --category multichannel --crs EPSG:3844
mspy project import Rupea /data/Rupea --type multichannel
```

## Survey

```text
mspy survey multichannel ...
mspy survey grid --protocol total-field ...
mspy survey grid --protocol fluxgate ...
```

### Multichannel

```bash
mspy survey multichannel --project PROJECT --format auto --workflow standard
```

The workflow preserves sensor/channel/session/source provenance where the input format supplies it. Normalized ASC is accepted by the established importer where appropriate.

### Total-field grid

```bash
mspy survey grid --project PROJECT --protocol total-field --workflow preservation
```

Optional derived gradient from split-sensor data:

```bash
mspy survey grid --project PROJECT --protocol total-field \
  --gradient vertical --sensor-separation METRES

mspy survey grid --project PROJECT --protocol total-field \
  --gradient horizontal --sensor-separation METRES
```

Relevant gradient controls include:

```text
--gradient none|vertical|horizontal
--sensor-separation METRES
--gradient-column NAME|auto
--sensor1-column NAME|auto
--sensor2-column NAME|auto
--top-column NAME|auto
--bottom-column NAME|auto
--left-column NAME|auto
--right-column NAME|auto
--gradient-sign auto|sensor1-minus-sensor2|sensor2-minus-sensor1
```

### Fluxgate grid

```bash
mspy survey grid --project PROJECT --protocol fluxgate --workflow archaeology
```

## Layout

```bash
mspy layout gui --project PROJECT --protocol total-field
mspy layout gui --project PROJECT --protocol fluxgate
mspy layout validate --project PROJECT --protocol total-field
mspy layout validate --project PROJECT --protocol fluxgate
```

## Derived processing

```bash
mspy process interpolate --project PROJECT [options]
mspy process interpolate --project PROJECT --input measurements.asc [options]
mspy process clean --project PROJECT [options]
mspy process enhance --project PROJECT [options]
mspy process segment --project PROJECT [options]
mspy process thin --project PROJECT [options]
```

## Filtering

```bash
mspy filter observations --project PROJECT --from STAGE [options]
mspy filter raster --project PROJECT --from STAGE [options]
mspy filter raster --input raster.tif -o FILTERED [options]
```

## Analysis

```bash
mspy analyze survey --project PROJECT [--from STAGE]
mspy analyze lines --project PROJECT --from STAGE
mspy analyze sensors --project PROJECT --from STAGE
mspy analyze raster --project PROJECT --from STAGE
mspy analyze spectrum --project PROJECT --from STAGE
mspy analyze stages --project PROJECT --stages STAGE1,STAGE2
```

## Figures, export and Web GIS

```bash
mspy figure single --project PROJECT --from STAGE [options]
mspy export map --project PROJECT --from STAGE [options]
mspy web --project PROJECT
```

## Installation commands

```bash
python -m pip install magsurveypy
python -m pip install --upgrade magsurveypy
python -m pip uninstall magsurveypy
```

For exhaustive option-level help use:

```bash
mspy --help
mspy help all
mspy survey grid --help
mspy tools help-all
```
