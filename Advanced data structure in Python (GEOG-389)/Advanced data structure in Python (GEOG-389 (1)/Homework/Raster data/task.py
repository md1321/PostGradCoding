# Import rasterio and rasterio.plot
import rasterio as rio
import rasterio.plot as riopl

# Read dem_oahu.tif as raster
# Change the file path accordingly
raster = rio.open("C:/Users/yi/Documents/UH_work/Teaching/GEOG389/other_materials/data/dem_oahu.tif")

# please create a map with two different colors.
# One color represent innundated area and the other color represent safe area.
