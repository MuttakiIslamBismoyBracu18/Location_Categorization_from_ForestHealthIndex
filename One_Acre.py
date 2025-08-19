import geopandas as gpd
from shapely.geometry import box
import math
import os

# --- Step 1: Load Forest Boundary Shapefile ---
boundary_fp = "D:\DNR\Forest Health Index\Duncan_woods.shp"  # Replace with your full path if needed
forest = gpd.read_file(boundary_fp)

# Step 2: Project to UTM for accurate distance in meters (EPSG:32616 for Michigan)
forest = forest.to_crs(epsg=32616)

# --- Step 3: Define 1-acre grid size ---
grid_size = 60.7  # in meters (1 acre ≈ 60.7 x 60.7)

# --- Step 4: Get boundary extent ---
minx, miny, maxx, maxy = forest.total_bounds

# --- Step 5: Create grid cells ---
grid_cells = []
x = minx
while x < maxx:
    y = miny
    while y < maxy:
        grid = box(x, y, x + grid_size, y + grid_size)
        grid_cells.append(grid)
        y += grid_size
    x += grid_size

# --- Step 6: Convert grid to GeoDataFrame ---
grid_gdf = gpd.GeoDataFrame({'geometry': grid_cells}, crs=forest.crs)

# --- Step 7: Clip grid to forest boundary ---
grid_clipped = gpd.overlay(grid_gdf, forest, how='intersection')

# --- Step 8: Assign unique ID to each grid cell ---
grid_clipped['cell_id'] = range(1, len(grid_clipped) + 1)

# --- Step 9: Export as new shapefile ---
output_fp = "Duncan_woods_1acre_grid.shp"
grid_clipped.to_file(output_fp)

print(f"✅ 1-acre grid saved as: {output_fp}")
