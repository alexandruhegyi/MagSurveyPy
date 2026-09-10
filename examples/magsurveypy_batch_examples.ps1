# MagSurveyPy 1.0.0 PowerShell batch examples
# Developed by Alexandru Hegyi, PhD

$Projects = @("Rupea", "Noviodunum", "Foeni")
foreach ($Project in $Projects) {
    mspy analyze survey --project $Project
}

$GradientProjects = @("Rupea", "Noviodunum")
foreach ($Project in $GradientProjects) {
    mspy export map `
      --project $Project `
      --from INTERPOLATED `
      --display-range 10 `
      --magnetic-unit "nT/m" `
      --scale-bar-position outside-bottom-center `
      --north-position outside-top-right `
      --format png `
      --dpi 600
}

# Exact -10..+10 publication map with display-only tone enhancement.
# The magnetic GeoTIFF values are not modified.
# mspy export map --project Foeni `
#   --input "$HOME/MagSurveyPy_Projects/Foeni/Results/TOTAL_FIELD/GeoTIFF/Foeni_total_field_archaeology.tif" `
#   --display-min -10 --display-max 10 `
#   --cmap gray_r `
#   --display-contrast 1.20 --display-brightness 1.05 --display-gamma 1.10 `
#   --colorbar-position right

# Preserve previous interpolation/map/figure variants
# mspy process interpolate --project Rupea --increment
# mspy figure single --project Rupea --from INTERPOLATED --display-std 2 --increment
# mspy export map --project Rupea --from INTERPOLATED --display-std 2 --increment
# mspy project history Rupea --category process --tail 20
