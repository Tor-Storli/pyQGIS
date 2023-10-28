# Import required modules
from qgis.core import (
    QgsVectorLayer, 
    QgsCoordinateReferenceSystem, 
    QgsCoordinateTransform,
    QgsFeature
)

# Load the original shapefile
input_path ="C:/users/storl/Desktop/QGIS_Scripts_2023/import/tl_rd22_us_county/tl_rd22_us_county.shp"

# Create a new Vector Layer using path to input states shapefile
US_Counties_Layer = iface.addVectorLayer(input_path,"US_COUNTIES","ogr")

# Filter the layer for counties in Illinois
US_Counties_Layer.setSubsetString("STATEFP = '17'")

# Set the CRS to NAD83 - East Illinois
crs = QgsCoordinateReferenceSystem("EPSG:3435")

IL_County_Layer = QgsVectorLayer('Polygon?crs=EPSG:3435', 'IL_COUNTIES', 'memory')

# Add fields from the original layer to the new layer
IL_County_Layer.dataProvider().addAttributes(US_Counties_Layer.fields())
IL_County_Layer.updateFields()

# Transform the features from the original layer to the new layer's CRS
transform = QgsCoordinateTransform(US_Counties_Layer.crs(), IL_County_Layer.crs(), QgsProject.instance())
for feature in US_Counties_Layer.getFeatures():
    geometry = feature.geometry()
    geometry.transform(transform)
    new_feature = QgsFeature(IL_County_Layer.fields())
    new_feature.setGeometry(geometry)
    new_feature.setAttributes(feature.attributes())
    IL_County_Layer.dataProvider().addFeature(new_feature)

# Save the new layer to a shapefile
output_file = "C:/Users/storl/Desktop/QGIS_Scripts_2023/export/IL_COUNTIES/IL_COUNTIES.shp"
QgsVectorFileWriter.writeAsVectorFormat(IL_County_Layer, output_file, 'utf-8', IL_County_Layer.crs(), 'ESRI Shapefile')
