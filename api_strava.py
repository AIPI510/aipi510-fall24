import geopandas as gpd
import matplotlib.pyplot as plt

if __name__=='__main__':
    """
    This is the main function to visualise the Strava Shapefiles as a graph plot.
 
    We use a desktop app called QGIS to visualise the Strava data. 
    This app lets us download our user data in format of a Shapefile. We use this Shapefile to plot a graph.
    We are reading the Shapefile using geopandas package and plot the data in a graph using matplotlib


    Requirements.txt:
    geopandas==0.12.2
    matplotlib==3.8.0

    Please install requirements.txt before running this script.

    """
    # Load the shapefile
    gdf = gpd.read_file("./shp/recent_activities.shp")
 
    # Plot the shapefile
    gdf.plot()
   
    # Show the plot
    plt.show()







