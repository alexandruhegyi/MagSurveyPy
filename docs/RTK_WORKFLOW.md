# RTK / GNSS Workflow — MagSurveyPy

**Developer:** Alexandru Hegyi, PhD  
**Website:** https://alexandruhegyi.com  
**Email:** alexandruhegyi@gmail.com  
**GitHub:** https://github.com/alexandruhegyi

The magnetic processing pipeline supports RINEX inspection, true RTKLIB PPK, static-base solving and radio-RTK base-coordinate shifts. These positioning tools are independent of the magnetic value processing.

## Inspect GNSS inputs

Use `mspy gnss --help` and `mspy guide rtk` for the exact subcommands available in this build.

## True PPK with RTKLIB

Install `rnx2rtkp`, verify it is in `PATH`, then solve the rover against a known base and navigation data. Example pattern:

```bash
mspy gnss ppk   --rover-obs rover.obs   --base-obs base.obs   --nav brdc.nav   --base-llh LAT LON HEIGHT   -o survey.pos
```

Apply a solved position file to PRM processing with the relevant `--rinex-position-solution` option.

## Static base solution

A static base can be solved relative to a reference station when the base coordinate was not known accurately in the field. Review ambiguity/fix quality and do not treat a low-quality float solution as centimetric truth.

## Radio-RTK base shift

If acquisition already used RTK relative positioning but the base was entered at an incorrect absolute coordinate, compute one rigid base-coordinate shift:

```bash
mspy gnss base-shift   --field-base-llh LAT_USED LON_USED H_USED   --corrected-base-llh LAT_TRUE LON_TRUE H_TRUE   -o base_shift.json
```

Then apply the shift during PRM processing. This changes absolute position, not relative sensor geometry.

## Do not double-correct

Do not apply a full PPK trajectory and a radio-RTK base shift to the same coordinates unless you have a specific geodetic reason. They represent different correction models.

## CRS

GNSS starts in geographic coordinates; PRM processing can choose local UTM automatically or use an explicit CRS such as `EPSG:32635`. Use `reproject` for deliverables in WGS84 or another CRS after the quantitative raster exists.

## External dependency

`rnx2rtkp` is classified by `doctor` as EXTERNAL. Its absence does not disable magnetic processing.
