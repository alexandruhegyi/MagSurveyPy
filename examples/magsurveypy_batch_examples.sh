#!/usr/bin/env bash
# MagSurveyPy 1.0.1 batch examples
# Developed by Alexandru Hegyi, PhD
# Edit project names/parameters before running.
set -euo pipefail

# Example 1 — analyze several projects without changing data.
for PROJECT in Rupea Noviodunum Foeni; do
  mspy analyze survey --project "$PROJECT"
done

# Example 2 — build comparable ±10 publication maps for two gradient projects.
for PROJECT in Rupea Noviodunum; do
  mspy export map \
    --project "$PROJECT" \
    --from INTERPOLATED \
    --display-range 10 \
    --magnetic-unit nT/m \
    --scale-bar-position outside-bottom-center \
    --north-position outside-top-right \
    --format png \
    --dpi 600
done

# Example 3 — preserve two alternative low-pass products.
INPUT="$HOME/MagSurveyPy_Projects/Noviodunum/Results/NewProcessing/GeoTIFF/Noviodunum_interpolated.tif"
OUT="$HOME/MagSurveyPy_Projects/Noviodunum/Results/LOW_PASS_TESTS"
mkdir -p "$OUT"
for SPEC in "02 0.2" "05 0.5"; do
  set -- $SPEC
  mspy filter raster --project Noviodunum --input "$INPUT" -o "$OUT" \
    --site-name "Noviodunum_LP$1" --low-pass "$2"
done

# Exact -10..+10 publication map with display-only tone enhancement.
# The magnetic GeoTIFF values are not modified.
# mspy export map --project Foeni \
#   --input "$HOME/MagSurveyPy_Projects/Foeni/Results/TOTAL_FIELD/GeoTIFF/Foeni_total_field_archaeology.tif" \
#   --display-min -10 --display-max 10 \
#   --cmap gray_r \
#   --display-contrast 1.20 --display-brightness 1.05 --display-gamma 1.10 \
#   --colorbar-position right

# Preserve previous interpolation/map/figure variants
# mspy process interpolate --project Rupea --increment
# mspy figure single --project Rupea --from INTERPOLATED --display-std 2 --increment
# mspy export map --project Rupea --from INTERPOLATED --display-std 2 --increment
# mspy project history --project Rupea --category process --tail 20
