# SENSYS PRM Guide — MagSurveyPy Version 1.0.3

## Purpose

This guide describes the production SENSYS/MonSX PRM importer used by MagSurveyPy.

## Magnetic word reconstruction

For the supported FGM650 PRM layout, each magnetic sample is a 16-bit word containing two distinct fields:

- high byte: fine phase, 0..255;
- low byte: modulo-256 coarse cycle counter.

MagSurveyPy unwraps the coarse counter first and reconstructs the full phase as:

```text
phase = fine + 256 × coarse_unwrapped
magnetic_value = phase × scale
```

The default scale is 0.07. This preserves fast, strong dipoles that can be folded by applying a nearest-cycle unwrap directly to the combined phase.

## GPS allocation

The fixed PRM header contains the initial GPS fix. Every following PRM record contains the endpoint GPS fix for its 50 magnetic samples. Therefore:

```text
GPS0 ---- 50 samples ---- GPS1 ---- 50 samples ---- GPS2 ...
```

Sample positions are interpolated in acquisition order between those boundary fixes. No anomaly-based time shift is applied by default.

## Probe geometry

Probe offsets are read from the PRM header. MagSurveyPy does not assume a fixed probe count or a fixed 0.50 m spacing. DeltaX is projected on the right-hand perpendicular to the local direction of travel and DeltaY on the forward direction. The default local heading uses a 1.5 m trajectory-smoothing window.

## Stationary acquisition blocks

The production default rejects a complete 50-sample block only when the embedded GPS moves less than 0.05 m from that block's start fix to its endpoint fix. This conservative gate removes unsupported start/stop acquisition while preserving moving survey data.

Use:

```bash
--stationary-block-filter off
```

to retain every recorded block, or change the threshold with:

```bash
--stationary-block-min-movement METRES
```

## Sidecar files

SENSYS exports can also contain `.disp`, `.cfg`, TXT, SHP, DXF or DLM products. These are useful independent references and may remain in the import folder. The production PRM decoder does not require them because probe geometry and GPS block structure are present in the PRM itself.

## Unsupported variants

PRM variants whose header, probe count or record size do not satisfy the supported structure are rejected with an explicit error. MagSurveyPy does not silently reinterpret unknown binary layouts.
