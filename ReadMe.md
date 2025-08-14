# README.md

## Project Title
**Forest Health Index (FHI) & Stand Health Index (SHI) Calculation and Visualization for Duncan Woods**

## Overview
This project calculates and visualizes the Forest Health Index (FHI) and Stand Health Index (SHI) for Duncan Woods using Sentinel-2 satellite imagery, GEDI LiDAR data, stability analysis, and advanced classification methods. The workflow integrates QGIS for polygon preparation, Google Earth Engine (GEE) for NDVI extraction, Python for data processing, and Kepler.gl for visualization.

---

## Features
- **NDVI Extraction** from Sentinel-2 imagery using GEE.
- **Min–Max Normalization** of NDVI, canopy height, and canopy cover.
- **FHI Calculation** combining NDVI, height, and cover.
- **Stability Integration** using multi-year NDVI standard deviation.
- **Updated_FHI** via harmonic mean penalizing low stability.
- **Classification** into health categories based on mean ± standard deviation.
- **SHI Calculation** following Das (2024) methodology.
- **Interactive Map Visualization** in Kepler.gl.

---

## Workflow Summary

### 1. **QGIS Preparation**
1. Install QGIS ([qgis.org](https://qgis.org)).
2. Load basemap (Google Satellite or OpenStreetMap via XYZ Tiles).
3. Create polygon layer → Shapefile → Polygon, CRS: EPSG:4326.
4. Digitize Area of Interest (AOI) for Duncan Woods.
5. Save as `Duncan_woods_1acre_grid.shp`.
6. Upload shapefile to GEE assets.

### 2. **GEE NDVI Extraction**
- Uses Sentinel-2 Level-2A imagery.
- NDVI formula: `(B8 - B4) / (B8 + B4)`.
- QA60 cloud masking applied.
- Monthly median NDVI computed and exported to Google Drive.
- **Script:** [`GEE_Code.txt`](./GEE_Code.txt).

### 3. **Local Data Processing in Python**
- Load CSV from Google Drive export.
- Replace invalid values (-9999) with NaN.
- Normalize NDVI, canopy height, and cover.
- Compute `FHI` as mean of normalized metrics.
- Compute `Stability_norm` from yearly NDVI std.
- Calculate `Updated_FHI` using harmonic mean.
- Categorize into health classes using μ and σ thresholds.
- Save final CSV for visualization.

### 4. **Kepler.gl Visualization**
1. Prepare CSV with `cell_id`, `.geo`, `Updated_FHI`, `FHI_Category`.
2. Upload to [kepler.gl](https://kepler.gl).
3. Add polygon layer, color by `FHI_Category`.
4. Adjust style and export as HTML/PNG.

---

## Classification Scheme
| Category           | Condition                                       |
|--------------------|--------------------------------------------------|
| Severely Stressed  | ≤ μ−1.5σ or FHI < 0.4                            |
| Stressed           | μ−1.5σ to μ−1.0σ                                 |
| Slightly Stressed  | μ−1.0σ to μ                                      |
| Moderately Healthy | μ to μ+1.0σ                                      |
| Healthy            | μ+1.0σ to μ+1.5σ                                 |
| Very Healthy       | > μ+1.5σ                                         |

---

## Outputs
Example June 2025 category ranges:
| Category           | Min    | Max    |
|--------------------|--------|--------|
| Severely Stressed  | 0.5609 | 0.5825 |
| Stressed           | 0.5842 | 0.6093 |
| Slightly Stressed  | 0.6115 | 0.6603 |  
| Moderately Healthy | 0.6609 | 0.7115 |
| Healthy            | 0.7121 | 0.7366 |
| Very Healthy       | 0.7377 | 0.7804 |

---

## Requirements
- QGIS (latest)
- Google Earth Engine account
- Python 3.x with:
  - pandas
  - numpy
  - geopandas
  - matplotlib
- Kepler.gl account

---

## References
- Dash, 2018 — *UAV Multispectral Imagery for Forest Health Monitoring*
- Das, 2024 — *Modeling Forest Canopy Structure and Stand Health Index*

