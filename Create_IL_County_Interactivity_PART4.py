"""
Here we are creating a custom map tool that inherits from QgsMapTool 
and overrides the canvasReleaseEvent method. 
This method will be called whenever you click on the map canvas. 

This custom map tool takes two arguments: 
  1) Canvas, which is the map canvas, and 
  2) Layer, which is the vector layer containing the county polygons. 

The canvasReleaseEvent method is called whenever you click on the map canvas. 

The pyQGIS script gets the click location, transforms it to map coordinates, 
and then finds the feature at that location. 
If a feature is found, the pyQGIS script gets the county name 
from the feature’s attributes and constructs a URL for the 
Wikipedia page for that county. 

Finally, The pyQGIS script opens the URL in a web browser 
using QDesktopServices.openUrl.

NOTE: Run the "Create_Color_and_Add_labels.py first to create a VectorLayer to work with!

"""


from qgis.gui import QgsMapTool

class CountyMapTool(QgsMapTool):
    def __init__(self, canvas, layer):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = layer

    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()

        # Transform the click to map coordinates
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        print(point)
        
        # Find the feature at the click location
        for feature in self.layer.getFeatures():
            if feature.geometry().contains(point):
                # Get the county name
                county_name = feature['NAME']
                # Open the wikipedia page for the county
                url = f'https://en.wikipedia.org/wiki/{county_name}_County,_Illinois'
                print("County_Name: ",county_name)
                print("Wiki-url: : ",url)
                
                QDesktopServices.openUrl(QUrl(url))
                break
                
# Get the map canvas and vector layer
canvas = iface.mapCanvas()
layers = QgsProject.instance().mapLayersByName("IL_COUNTIES")
if layers:
    layer = layers[0]

# Create an instance of the custom map tool
tool = CountyMapTool(canvas, layer)

# Set the custom map tool as the active map tool for the map canvas
canvas.setMapTool(tool)
