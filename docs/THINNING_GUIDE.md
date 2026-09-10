# Physical Track Thinning Guide — MagSurveyPy

**Developer:** Alexandru Hegyi, PhD  
**Website:** https://alexandruhegyi.com  
**Email:** alexandruhegyi@gmail.com  
**GitHub:** https://github.com/alexandruhegyi

## What physical thinning means

Physical thinning selects a subset of **real measured sensor trajectories**. It is not raster downsampling and it is not interpolation. Coordinates and magnetic measurements of retained points are not shifted to an ideal lattice.

## Native sensor spacing and sensor lanes

A multichannel cart can carry several sensors at a known physical separation. During straight acquisition each sensor describes a lane. A nominal 0.25 m five-sensor configuration can therefore create dense parallel trajectories, but turns, swath overlap, navigation noise and crossings make a site-wide even/odd file-index rule unreliable.

## Swath reconstruction

MagSurveyPy reconstructs stable straight survey portions and groups them by orientation. Tiny fragments and turns should not define the thinning lattice. Sensor-segment overlap cleaning is performed first so duplicate measurements do not bias spacing estimates.

## Cross-track projection

For each orientation family, the local survey heading defines an along-track and cross-track coordinate system. Track spacing is evaluated in cross-track coordinates, while local overlap/support is checked along the acquisition direction.

## Phase selection

For a native 0.25 m to target 0.50 m request, the basic physical choice is normally one of two phases. MagSurveyPy does not let each neighbouring swath choose phase independently without consequence. A swath-adjacency graph propagates a coherent phase preference while retaining the ability to handle physically irregular swaths.

## Conflict resolution

When retained measured trajectories are locally closer than the hard spacing threshold, the selector compares support/priority and clips the lower-priority **measured segment** in the conflict area. It does not move either line. Conflict counts and resolved counts are reported.

## Gap recovery

After conflict removal, the program searches unused real trajectory pieces. A candidate can be added only if it improves local spacing without recreating a close-pair conflict. Recovered pieces are counted. No missing line is synthesized.

## Gap classes

- **True unsupported gap:** no suitable measured trajectory exists locally.
- **Overlap/removal gap:** support was lost because duplicated/conflicting material was removed.
- **Unexplained/algorithm-created gap:** the selector created a gap where real support could reasonably have been retained. This is a strict-QC concern.

The distinction matters: a survey cannot be made physically regular where measurements were never collected.

## Crossings and secondary orientations

Orientation families are analysed separately. A crossing line is not treated as a 0.50 m neighbour of the dominant family. At intersections the real measurements remain available, but spacing statistics are calculated within the appropriate parallel family/support context.

## QC metrics

The report includes requested and native spacing, input/retained trajectory counts, retention fraction, mean/median/std/MAD, P05/P25/P75/P95, ±10/±20% fractions, counts below 0.35/0.40 m and above 0.60/0.75/1.0 m, phase transitions/switches, conflicts, conflicts resolved, gaps recovered, unsupported/unexplained gaps, spatial continuity and orientation-family metrics.

Outputs include CSV, TXT, JSON, PNG and a GeoPackage showing measured trajectory status.

## Strict / warn / force

### `--policy strict`
Recommended. A failed significant orientation family prevents the thinned candidate from becoming primary. The program prints:

```text
THINNING REJECTED FOR PRIMARY PRODUCT
```

and preserves native surviving physical tracks.

### `--policy warn`
Keeps a failed candidate for expert inspection. Not the conservative production default.

### `--policy force`
Deliberately uses a failed candidate. The program prints a prominent warning. Use only when you explicitly accept the geometry after independent inspection.

## Why median spacing is insufficient

A global median of ~0.50 m can coexist with many 0.25 m close pairs and 0.75–1.0+ m gaps. Archaeological sampling support is local. Strict QC therefore checks the full distribution and spatial continuity, not only the median.

## Rupea validation

Release validation on the uploaded Rupea export found 620 PRMs, of which 243 were byte-identical duplicates, leaving 377 unique acquisitions. Automatic geometry detected EPSG:32635, principal heading ~17.44°, native sensor spacing ~0.250 m and four orientation families.

For the dominant family, the final MagSurveyPy geometry-repair stage removed residual sub-0.35 m close-pair conflicts, leaving **0** such close-pair samples, achieved ~**91.0% within ±20% among locally supported adjacency samples**, and left one unexplained gap occurrence while separately identifying extensive genuinely unsupported geometry. Because the resulting candidate still required many controlled phase substitutions and the full local geometry was not sufficiently regular, strict policy rejected the 0.50 m candidate. That rejection is the correct scientific result for this dataset.

## Inspecting the GeoPackage

Load `Vectors/*_track_thinning_tracks.gpkg` in QGIS together with the native point/track products. Inspect retained/rejected/conflict/gap-recovery status at swath boundaries, turns and crossings. A good candidate should show consistent neighbouring selection without alternating parity jumps and without unexplained local holes.

## Fast QC-only command

```bash
mspy process thin --project Site -o Thin050_QC --spacing 0.50 --policy strict --qc-only --cores 8
```

This performs geometry/QC and vector/report export but skips the large PRM-to-ASC conversion.
