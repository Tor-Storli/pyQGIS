# Load libraries from QGIS
from qgis.core import (QgsSimpleFillSymbolLayer, 
                        QgsGradientFillSymbolLayer, 
                        QgsGradientColorRamp, 
                        QgsGradientStop, 
                        QgsColorRampShader
                        )

# Remove all existing Layers
for layer in QgsProject.instance().mapLayers().values(): 
        QgsProject.instance().removeMapLayer(layer.id()) 
iface.mapCanvas().refresh()

# Import IL_Counties shape file from local drive
path = 'C:/Users/storl/Desktop/QGIS_Scripts_2023/import/IL_COUNTIES.shp'

# Create a new layer from the imported shapefile
countyLayer = iface.addVectorLayer(path, 'IL_COUNTIES', 'ogr')

# Set Active Layer to be IL_Counties
iface.setActiveLayer(countyLayer)
layer = iface.activeLayer()

"""
Get the renderer from the active layer (which is set to ‘IL_COUNTIES’). 
This renderer can then be used to modify how the layer is drawn. 
For example, you can change the symbol used to represent the features in the layer
Here we will change the Symbol with colors and we will add labels
"""
renderer = layer.renderer()
symbol = renderer.symbol()

# Create gradient fill symbol layer
# symbol_layer = QgsGradientFillSymbolLayer()
# symbol_layer.setGradientType(QgsGradientType.TwoColor)

# Set gradient colors
# color1 = QColor(255, 165, 0)  # RGB for orange
# color2 = QColor(255, 140, 0)  # RGB for dark orange
# ramp = QgsGradientColorRamp(color1, color2)
# symbol_layer.setColorRamp(ramp)
# symbol.changeSymbolLayer(0, symbol_layer)

# Create a simple solid color layer
symbol_layer = QgsSimpleFillSymbolLayer()
symbol_layer.setColor(QColor(194,94,0))
symbol.changeSymbolLayer(0, symbol_layer)

# Create labels from the Name column in the Attributes table
label = QgsPalLayerSettings()
label.fieldName = "NAME"
label.enabled = True

layer.setLabelsEnabled(True)
layer.setLabeling(QgsVectorLayerSimpleLabeling(label))

# Refresh the canvas layer
layer.triggerRepaint()

