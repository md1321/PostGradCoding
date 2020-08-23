# Load the geopandas package, and name it gdp
import geopandas as gdp

# Read the shapefile crime.shp into data.
# Change the file path accordingly. You may copy from the previous task
data = gdp.read_file("type here")

# Get all unique offence types
data[type here].unique()


# Get all burglary incidents in Oahu.
data[data[type here]==type here]

# Read census tract boundaries in Oahu
# Change the file path accordingly
data_ct = gdp.read_file("type here")

# Create a map of the tract boundaries and assign the map to base1
base1 = data_ct.plot(color='white', edgecolor='black')

# Plot all these theft incidents in Oahu, using census tracts as the base map
data[type here].plot(ax=base1, marker='*', color='green', markersize=0.5)

# Create another map of the tract boundaries and assign the map to base2
base2 = data_ct.plot(color='white', edgecolor='black')

# Plot all graffiti incidents in Oahu.
type here

# Visually compare the spatial distributions of the two crime types in the maps (no need to write code here)
