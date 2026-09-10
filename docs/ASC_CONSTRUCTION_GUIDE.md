# ASC Construction Guide — MagSurveyPy Version 1.0.0

The ASC is the authoritative normalized measurement product for PRM projects.

## Production sequence

```text
PRM binary data
  -> native FGM phase reconstruction
  -> initial header GPS + record endpoint GPS
  -> sample-by-sample position interpolation
  -> local probe-frame orientation
  -> physical probe offsets
  -> conservative stationary-block gate
  -> optional overlap/thinning operations
  -> X, Y, magnetic value, source, probe ASC
```

Magnetic values are not inferred from a raster. Coordinates are not shifted according to the shape of magnetic anomalies.

The normal ASC columns are:

```text
X    Y    magnetic_value    source_prm    probe_id
```

The original PRM files remain unchanged in `RawData/Multichannel`.
