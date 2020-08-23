# Load the geopandas package, and name it gdp
import geopandas as gdp

# Read the crime data
# Change the file path accordingly.
data = gdp.read_file(type here)


# Read census tract boundaries in Oahu
# Change the file path accordingly
data_ct = gdp.read_file("type herect_oahu.shp")

# Create a map of the tract boundaries and assign the map to base
base = data_ct.plot(color='white', edgecolor='black')

# plot the crime data using census tract boundaries as the basemap
data.plot(ax=base, marker='o', color='red', markersize=0.5)
