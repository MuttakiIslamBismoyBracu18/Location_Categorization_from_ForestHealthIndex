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

# Forest Boundary and 1-Acre Grid Creation in QGIS

This document provides a **step-by-step guide** for creating a shapefile (`.shp`) of a forest boundary in QGIS, generating a **1-acre grid**, and ensuring that all associated shapefile components (`.cpg`, `.dbf`, `.prj`, `.shx`) are exported correctly.

---

## 🛠️ Requirements
- Install [QGIS](https://qgis.org) (Free & Open Source)
- Install the **QuickMapServices** plugin for base maps (satellite/OSM)

---

## 📍 Step 1: Open QGIS and Set Up a Basemap
1. Launch **QGIS**.  
2. Add a base map for reference:  
   - `Web → QuickMapServices → OSM` or `Google Satellite`.  
   - If QMS is not installed: `Plugins → Manage → Search for "QuickMapServices"` and install it.

---

## 🧱 Step 2: Create a New Shapefile Layer
1. Go to: `Layer → Create Layer → New Shapefile Layer…`  
2. Set parameters:
   - **Type**: Polygon  
   - **CRS**: Choose appropriate UTM (e.g., EPSG:32616 for West Michigan)  
   - **File name**: `Duncan_Woods.shp`  
   - Add optional fields (e.g., `Name` as Text)  
3. Click **OK** and save the new shapefile.

---

## ✏️ Step 3: Digitize the Forest Boundary
1. In the Layers Panel, select the new shapefile.  
2. Enter editing mode: click the **pencil icon 📝** (Toggle Editing).  
3. Use **Add Polygon Feature** tool to draw the forest boundary by clicking around it.  
   - Double-click to finish.  
   - Enter an ID or name when prompted.  
4. Adjust vertices with the Vertex Tool if needed.  

---

## 💾 Step 4: Save and Finish
1. Click the floppy disk icon 💾 → Save Layer Edits.  
2. Toggle off editing mode.  
3. You now have a polygon `.shp` file defining your forest boundary.

---

## 📤 Optional: Export to Other Formats
Right-click the layer → `Export → Save Features As…`  
- Export to `.geojson`, `.kml`, `.csv`, etc., if needed for Google Earth Engine or Python workflows.

---

## 🌲 Step 5: Generate 1-Acre Grid
1 acre ≈ **63.6 m × 63.6 m**  

### Method in QGIS:
1. Go to: `Vector → Research Tools → Create Grid`.  
2. Parameters:
   - **Grid type**: Rectangle (Polygon)  
   - **Extent**: Select your forest boundary layer  
   - **Grid spacing**: 63.6 m (X and Y)  
   - **CRS**: Same as boundary layer (UTM projection)  
   - **Output**: Save as `Duncan_Woods_Grid.shp`  
3. Clip the grid to boundary:  
   - `Vector → Geoprocessing Tools → Clip`  
   - Input: grid  
   - Overlay: forest boundary  
   - Save output: `Duncan_Woods_1AcreGrid.shp`

---

## 🔑 Step 6: Add Cell Identifiers
1. Open the Attribute Table of the clipped grid.  
2. Use **Field Calculator** → Create new field: `cell_id`.  
3. Expression: `$rownum` (auto-assigns unique ID to each 1-acre polygon cell).  

---

## 🐍 Step 7: Code Example to Automate in Python
You can also create the **1-acre grid** programmatically using PyQGIS: **Script:** [`One_Acre.py`](./One_Acre.py)

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

