import os

# Set up import and export filenames and paths
wd = 'C:/Users/storl/Desktop/QGIS_Scripts_2023/export/IL_COUNTIES/'

 # Change the directory
os.chdir(wd) # Change the directory

 # load shapefile
fname = wd + 'IL_COUNTIES.shp'
outfile = wd + '/QGIS_DEMO_AREA/IL_COUNTIES_AREA.shp'  # save shapefile

# Remove all existing Layers
for layer in QgsProject.instance().mapLayers().values(): 
        QgsProject.instance().removeMapLayer(layer.id()) 
iface.mapCanvas().refresh()

 # load shapefile
layer = iface.addVectorLayer(fname,'','ogr')
pv = layer.dataProvider()

#Create a list of the valid Fieldsyou want
lstValidFields = ['STATEFP', 'COUNTYFP', 'COUNTYNS', 'GEOID', 'NAME', 'NAMELSAD', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON']

#Get All Field names that exists in layer
lstAllFields = layer.fields().names()
	
#Delete these fields from Attribute table using list comprehension
lstDelFields = [item for item in lstAllFields if item not in lstValidFields]
#print(lstDelFields)

def deleteField(fldname):
    with edit(layer):
        idx = layer.fields().indexFromName(fldname)
        layer.dataProvider().deleteAttributes([idx])
    
    # Update layer 
    layer.updateFields()
    return

# Call deleteField and pass each fieldname that needs to be removed from the Attribute table
for fldname in lstDelFields:
    deleteField(fldname)

# Add new field names to the Attribute table using the dataProvider (pv)
pv.addAttributes([QgsField('TOTAL_AREA',QVariant.LongLong), \
QgsField('AREA_KM',QVariant.Int), \
QgsField('AREA_MI',QVariant.Int),
QgsField('GEOM_KM',QVariant.Int), \
QgsField('GEOM_MI',QVariant.Int),
])
                
layer.updateFields()
#-----------------------------------------------------------------------------------------------------------------------------------
# Create calculation expressionsusing fields grom the attribute table where:
# 1) 'ALAND'  = 'Land Area'
# 2) 'AWATER'  = 'Water Area'
# 3) Total Area =  ("ALAND" + "AWATER")
# 4) Conversion Factor for square meters to square Miles:   0.0000003861
# **Note:  Both fields are calculated by the US Census Bureau and the measurement is in Square feet
# ----------------------------------------------------------------------------------------------------------------------------------

areaTotal = QgsExpression('"ALAND" + "AWATER"')
areaKM = QgsExpression('Round((("ALAND" + "AWATER") * 0.000001),-1)')
areaMI = QgsExpression('Round((("ALAND" + "AWATER") * 0.0000003861),0)')

# . The $area variable is a special field name that QGIS interprets as the area of the geometry. 
areaKMGeom = QgsExpression('Round(($area * 0.000001),-1)')
areaMIGeom = QgsExpression('Round(($area * 0.0000003861),0)')
#
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

lstNewFields = [('TOTAL_AREA',areaTotal),('AREA_KM',areaKM),('AREA_MI',areaMI),('GEOM_KM',areaKMGeom),('GEOM_MI',areaMIGeom)]

def sddNewField(fldname, fieldFormula):
    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f[fldname] = fieldFormula.evaluate(context)
            layer.updateFeature(f)

for fld in lstNewFields:
    sddNewField(fld[0], fld[1])

# write the output to Disk - ESRI Shape file format
QgsVectorFileWriter.writeAsVectorFormat(layer, outfile, "utf-8", layer.crs(), "ESRI Shapefile")