# Import rasterio and rasterio.plot
import rasterio as rio
import rasterio.plot as riopl

# Read dem_oahu.tif as raster
# Change the file path accordingly
raster = rio.open("C:/Users/yi/Documents/UH_work/Teaching/GEOG389/other_materials/data/dem_oahu.tif")
