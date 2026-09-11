# MagSurveyPy 1.0.1 — Raster Georeferencing Guide

## Purpose

Archaeological total-field and fluxgate surveys are often processed first in a local survey grid. The magnetic raster may therefore have meaningful local X/Y geometry but no real-world CRS. MagSurveyPy provides a control-point georeferencer so that these quantitative rasters can be placed on the Web GIS map without altering their magnetic values.

The georeferencer is designed for survey grids whose relationship to GPS/map coordinates can be represented by one **2-D affine transform** (translation, rotation, independent X/Y scale and shear). This is normally appropriate for rectangular archaeological survey grids measured with GPS control points.

## Scientific principle

The first georeferencing step does **not resample the magnetic raster**. MagSurveyPy fits an affine transform from the control points and writes the original raster array unchanged to a new GeoTIFF with that transform and CRS.

A later CRS conversion is a separate, explicit operation:

```bash
mspy export reproject \
  --project SITE \
  --input /path/to/georeferenced.tif \
  --epsg 32634
```

Reprojection necessarily resamples the spatial grid, so keeping it separate makes the processing history transparent.

## Web GIS workflow

Launch:

```bash
mspy web --project SITE
```

Open **Georef**.

1. Select an unreferenced project TIFF.
2. Enter the CRS of the coordinates you will type:
   - `EPSG:4326` for longitude/latitude.
   - A projected CRS such as `EPSG:32634` for UTM Easting/Northing.
3. Open the control-point editor.
4. Use **Fit**, **100%**, **Zoom −** and **Zoom +** to inspect the raster. You can also use **Ctrl + mouse wheel** to zoom around the pointer. Pan normally with the scrollbars when zoomed in.
5. Click the exact known location on the raster. GCP placement is continuous and **does not snap** to an integer pixel or grid.
6. Enter the corresponding target X/Y coordinates.
7. Repeat for at least three points.
8. Press **Fit / check residuals**.
9. Inspect the RMSE, maximum residual and each point residual.
10. Correct/delete suspicious points if necessary.
11. Press **Write georeferenced GeoTIFF**.

The output is stored under:

```text
PROJECT/Results/GEOREFERENCED/
```

and is immediately added as a normal Web GIS raster layer.

## Number and distribution of control points

- **3 points**: mathematical minimum for an affine solution.
- **4–8 points**: recommended for most archaeological surveys.
- More points are useful when they are accurate and well distributed.

Do not place all control points along one line. Prefer points around the survey perimeter/corners plus one or more internal checks when available.

For an overdetermined solution (4+ points), MagSurveyPy solves one least-squares affine transform from all control points and reports the residual at every point.

## Control-point coordinates

The clicked image location is recorded as a continuous full-resolution raster column/row coordinate. The editor uses one shared raster stage for the image, click transform and GCP overlay, so the visible marker remains at the exact location that was clicked at every zoom level.

The preview may be downsampled for browser performance, but clicks are converted back to the original raster dimensions as continuous floating-point coordinates. They are not rounded or snapped. Zooming changes only the browser view; it does not alter GCP coordinates.

Target coordinates must all use the same CRS.

Examples:

```text
EPSG:4326
X = longitude
Y = latitude
```

or:

```text
EPSG:32634
X = Easting
Y = Northing
```

## QC outputs

Beside every georeferenced TIFF, MagSurveyPy writes:

```text
survey_georeferenced.tif
survey_georeferenced.gcps.csv
survey_georeferenced.georef.json
```

The CSV contains the entered point coordinates, fitted coordinates and residuals.

The JSON recipe records:

- source raster
- target CRS
- affine transform
- complete GCP list
- GCP count
- RMSE
- maximum residual
- approximate pixel dimensions
- application/version
- confirmation that magnetic values were not resampled

This recipe is intended to make georeferencing reproducible for publications and data archives.

## CLI georeferencing

The Web GIS saves a `.gcps.csv`, but a GCP file can also be prepared manually with columns:

```csv
col,row,x,y
0,0,596000,6837000
160,0,596040,6837000
0,160,596000,6836960
160,160,596040,6836960
```

Then run:

```bash
mspy project georeference --project SITE \
  --input /path/to/unreferenced.tif \
  --gcps /path/to/control_points.csv \
  --crs EPSG:32634
```

Default output:

```text
PROJECT/Results/GEOREFERENCED/<source>_georeferenced.tif
```

Custom output:

```bash
mspy project georeference --project SITE \
  --input /path/to/unreferenced.tif \
  --gcps control_points.csv \
  --crs EPSG:32634 \
  -o SITE_GPS_georeferenced.tif
```

## Reprojecting afterward

Once the TIFF has a valid CRS:

```bash
mspy export reproject \
  --project SITE \
  --input ~/MagSurveyPy_Projects/SITE/Results/GEOREFERENCED/SITE_GPS_georeferenced.tif \
  --epsg 4326
```

or, for a Norwegian UTM output:

```bash
mspy export reproject \
  --project SITE \
  --input ~/MagSurveyPy_Projects/SITE/Results/GEOREFERENCED/SITE_GPS_georeferenced.tif \
  --epsg 32634
```

## When affine georeferencing is not appropriate

Do not use this affine tool to compensate for severe non-linear image distortion, scanner warping, or irregularly rubber-sheeted historic maps. Those cases require polynomial or thin-plate-spline warping and should be treated as a different operation because they resample the raster geometry.

For normal magnetic survey grids exported from acquisition/processing software, affine GCP georeferencing is intentionally the default because it is simple, auditable and preserves the original quantitative raster values.
