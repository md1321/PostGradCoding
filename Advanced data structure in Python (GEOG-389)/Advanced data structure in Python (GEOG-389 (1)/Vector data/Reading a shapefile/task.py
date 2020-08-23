# Load the geopandas package, and name it gdp
type here geopandas type here gdp

# Read the shapefile crime.shp into data.
# Change the file path accordingly.
data = gdp.read_file(type here)

# Print the type of data
type here

# Print the first 5 rows of data
type here

# plot the geometries (point) of the data
data.plot()

# Plot the data again with different symbols and colors
data.plot(marker='*', color='green', markersize=0.5)


