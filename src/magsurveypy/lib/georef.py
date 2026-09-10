"""Ground-control-point georeferencing for MagSurveyPy.

This module deliberately implements a transparent affine GCP solution.  It is
well suited to archaeological survey grids that have been exported in local
pixel/grid coordinates but for which several GPS control points are known.

The source magnetic values are never interpolated or rescaled by the affine
assignment itself: the source array is copied unchanged and receives a fitted
GeoTIFF affine transform + CRS.  Reprojection/warping, when desired, remains a
separate explicit export operation.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
import csv
import json
import math
import time

import numpy as np


@dataclass
class GCPFit:
    transform: object
    residuals: list[dict]
    rmse: float
    max_residual: float
    mean_residual: float
    rmse_pixels: float | None
    pixel_size_x: float
    pixel_size_y: float
    determinant: float
    target_crs: str
    geographic: bool
    rmse_m: float | None = None
    max_residual_m: float | None = None


def _normalise_point(p: dict, index: int) -> dict:
    aliases = {
        "col": ("col", "column", "pixel_x", "px", "image_x"),
        "row": ("row", "pixel_y", "py", "image_y"),
        "x": ("x", "easting", "lon", "longitude", "target_x"),
        "y": ("y", "northing", "lat", "latitude", "target_y"),
    }
    out = {}
    lower = {str(k).strip().lower(): v for k, v in p.items()}
    for dst, names in aliases.items():
        value = None
        for n in names:
            if n in lower and lower[n] not in (None, ""):
                value = lower[n]
                break
        if value is None:
            raise ValueError(f"Control point {index + 1} is missing {dst}.")
        try:
            out[dst] = float(value)
        except Exception as exc:
            raise ValueError(f"Control point {index + 1} has invalid {dst}: {value!r}") from exc
    out["label"] = str(lower.get("label") or lower.get("name") or f"GCP {index + 1}")
    return out


def normalise_points(points: Iterable[dict]) -> list[dict]:
    pts = [_normalise_point(dict(p), i) for i, p in enumerate(points)]
    if len(pts) < 3:
        raise ValueError("Affine georeferencing requires at least 3 control points.")
    # Coincident image or target points make the affine solution ill-conditioned.
    pix = {(round(p["col"], 9), round(p["row"], 9)) for p in pts}
    xy = {(round(p["x"], 12), round(p["y"], 12)) for p in pts}
    if len(pix) < 3:
        raise ValueError("At least 3 distinct image control-point locations are required.")
    if len(xy) < 3:
        raise ValueError("At least 3 distinct target-coordinate locations are required.")
    return pts


def fit_affine(points: Sequence[dict], target_crs: str) -> GCPFit:
    """Fit x=a*col+b*row+c, y=d*col+e*row+f by least squares."""
    from affine import Affine
    from pyproj import CRS, Geod

    pts = normalise_points(points)
    crs = CRS.from_user_input(target_crs)
    A = np.array([[p["col"], p["row"], 1.0] for p in pts], dtype=float)
    tx = np.array([p["x"] for p in pts], dtype=float)
    ty = np.array([p["y"] for p in pts], dtype=float)
    if np.linalg.matrix_rank(A) < 3:
        raise ValueError("Image control points are collinear; choose points spread across the raster.")
    cx, *_ = np.linalg.lstsq(A, tx, rcond=None)
    cy, *_ = np.linalg.lstsq(A, ty, rcond=None)
    a, b, c = map(float, cx)
    d, e, f = map(float, cy)
    transform = Affine(a, b, c, d, e, f)
    det = float(a * e - b * d)
    if not np.isfinite(det) or abs(det) < 1e-18:
        raise ValueError("Control points produced a singular/degenerate affine transform.")

    px = float(math.hypot(a, d))
    py = float(math.hypot(b, e))
    pred_x = A @ cx
    pred_y = A @ cy
    residuals = []
    dist = np.hypot(pred_x - tx, pred_y - ty)
    rmse = float(math.sqrt(float(np.mean(dist ** 2))))
    mean_res = float(np.mean(dist))
    max_res = float(np.max(dist))
    mean_pix = (px + py) / 2.0 if px > 0 and py > 0 else float("nan")
    rmse_pix = float(rmse / mean_pix) if np.isfinite(mean_pix) and mean_pix > 0 and not crs.is_geographic else None

    rmse_m = None
    max_m = None
    meter_residuals = None
    if crs.is_geographic:
        try:
            geod = Geod(ellps="WGS84")
            meter_residuals = []
            for x0, y0, x1, y1 in zip(tx, ty, pred_x, pred_y):
                _, _, dd = geod.inv(float(x0), float(y0), float(x1), float(y1))
                meter_residuals.append(abs(float(dd)))
            rmse_m = float(math.sqrt(np.mean(np.square(meter_residuals))))
            max_m = float(max(meter_residuals))
        except Exception:
            meter_residuals = None

    for i, (p, xp, yp, rr) in enumerate(zip(pts, pred_x, pred_y, dist)):
        rec = {
            **p,
            "predicted_x": float(xp),
            "predicted_y": float(yp),
            "residual": float(rr),
            "residual_x": float(xp - p["x"]),
            "residual_y": float(yp - p["y"]),
        }
        if meter_residuals is not None:
            rec["residual_m"] = float(meter_residuals[i])
        residuals.append(rec)

    return GCPFit(
        transform=transform,
        residuals=residuals,
        rmse=rmse,
        max_residual=max_res,
        mean_residual=mean_res,
        rmse_pixels=rmse_pix,
        pixel_size_x=px,
        pixel_size_y=py,
        determinant=det,
        target_crs=crs.to_string(),
        geographic=bool(crs.is_geographic),
        rmse_m=rmse_m,
        max_residual_m=max_m,
    )


def read_gcps_csv(path: str | Path) -> list[dict]:
    q = Path(path).expanduser().resolve()
    if not q.exists():
        raise FileNotFoundError(q)
    with q.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return normalise_points(rows)


def write_gcps_csv(path: str | Path, points: Sequence[dict], residuals: Sequence[dict] | None = None) -> Path:
    q = Path(path)
    q.parent.mkdir(parents=True, exist_ok=True)
    rows = list(residuals) if residuals is not None else normalise_points(points)
    fields = ["label", "col", "row", "x", "y", "predicted_x", "predicted_y", "residual_x", "residual_y", "residual", "residual_m"]
    with q.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return q


def _safe_stem(text: str) -> str:
    import re
    s = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(text).strip()).strip("._")
    return s or "georeferenced"


def georeference_tiff(
    source: str | Path,
    output: str | Path,
    points: Sequence[dict],
    target_crs: str,
    *,
    recipe_path: str | Path | None = None,
    gcp_csv_path: str | Path | None = None,
    software: str = "MagSurveyPy",
    version: str = "1.0.0",
) -> dict:
    """Assign a least-squares affine transform and CRS without resampling values."""
    import rasterio
    from pyproj import CRS

    src = Path(source).expanduser().resolve()
    dst = Path(output).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    pts = normalise_points(points)
    fit = fit_affine(pts, target_crs)
    crs = CRS.from_user_input(target_crs)

    with rasterio.open(src) as ds:
        if ds.count < 1:
            raise ValueError("Source raster contains no bands.")
        profile = ds.profile.copy()
        # Remove storage hints that can become invalid when copied across drivers.
        for k in ("blockxsize", "blockysize", "tiled"):
            profile.pop(k, None)
        profile.update(driver="GTiff", crs=crs.to_wkt(), transform=fit.transform, compress="deflate")
        with rasterio.open(dst, "w", **profile) as od:
            for band in range(1, ds.count + 1):
                od.write(ds.read(band), band)
                if ds.descriptions and ds.descriptions[band - 1]:
                    od.set_band_description(band, ds.descriptions[band - 1])
            tags = ds.tags()
            if tags:
                od.update_tags(**tags)
            od.update_tags(
                software=software,
                version=version,
                georeferencing="affine_gcp_least_squares",
                georeferencing_source=str(src),
                georeferencing_target_crs=crs.to_string(),
                georeferencing_gcp_count=str(len(pts)),
                georeferencing_rmse=f"{fit.rmse:.12g}",
                georeferencing_max_residual=f"{fit.max_residual:.12g}",
                georeferencing_values_resampled="NO",
            )

    if gcp_csv_path is None:
        gcp_csv_path = dst.with_suffix(".gcps.csv")
    gcp_csv = write_gcps_csv(gcp_csv_path, pts, fit.residuals)
    recipe = {
        "application": software,
        "version": version,
        "operation": "affine_gcp_georeference",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": str(src),
        "output": str(dst),
        "target_crs": crs.to_string(),
        "transform": [float(x) for x in tuple(fit.transform)[:6]],
        "gcp_count": len(pts),
        "rmse": fit.rmse,
        "mean_residual": fit.mean_residual,
        "max_residual": fit.max_residual,
        "rmse_pixels": fit.rmse_pixels,
        "rmse_m": fit.rmse_m,
        "max_residual_m": fit.max_residual_m,
        "pixel_size_x": fit.pixel_size_x,
        "pixel_size_y": fit.pixel_size_y,
        "values_resampled": False,
        "control_points": fit.residuals,
        "gcp_csv": str(gcp_csv),
    }
    if recipe_path is None:
        recipe_path = dst.with_suffix(".georef.json")
    recipe_q = Path(recipe_path)
    recipe_q.parent.mkdir(parents=True, exist_ok=True)
    recipe_q.write_text(json.dumps(recipe, indent=2), encoding="utf-8")
    return {"output": dst, "gcp_csv": gcp_csv, "recipe": recipe_q, "fit": fit, "metadata": recipe}


def default_output_name(source: str | Path) -> str:
    return f"{_safe_stem(Path(source).stem)}_georeferenced.tif"
