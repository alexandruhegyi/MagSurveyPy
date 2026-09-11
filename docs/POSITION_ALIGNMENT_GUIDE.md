# SENSYS Position Allocation Guide — MagSurveyPy Version 1.0.3

The production PRM workflow uses the timing and GPS structure embedded in the PRM directly.

The initial GPS fix comes from the fixed header and each record supplies the endpoint fix for the following 50-sample acquisition interval. Magnetic samples are interpolated between those boundary fixes in their recorded order.

Default:

```bash
--position-alignment off
```

This means no magnetic-anomaly-derived coordinate shift is applied. The optional `auto` mode is retained only as an explicit advanced crossover experiment and is not part of the normal SENSYS workflow.

Probe offsets are rotated using the local travel direction. The default `--frame-heading smooth --heading-window 1.5` follows the local trajectory while suppressing centimetre-scale GNSS heading jitter.
