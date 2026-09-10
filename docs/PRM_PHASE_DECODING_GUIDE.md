# PRM Phase Decoding Guide — MagSurveyPy Version 1.0.0

The SENSYS FGM650 magnetic sample word is decoded as two fields rather than treated as a conventional wrapped scalar.

```text
high byte -> fine phase
low byte  -> modulo-256 coarse cycle counter
```

The coarse counter is unwrapped through its modulo boundary and the full phase is reconstructed as `fine + 256*coarse`. The magnetic scale is then applied.

This matters most near strong ferrous/dipolar anomalies. A direct nearest-cycle unwrap of the combined phase can choose the wrong integer branch when the field changes rapidly between adjacent samples. Reconstructing the native fine/coarse representation preserves those large excursions.

The default mode is:

```bash
--phase-repair sensys-native
```

An optional `persistent-step` diagnostic remains available for unusual datasets, but the normal workflow does not force strong responses onto a neighbouring phase branch.
