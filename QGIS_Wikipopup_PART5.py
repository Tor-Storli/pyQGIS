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

from qgis.PyQt.QtWidgets import QMessageBox, QTextBrowser
from PyQt5.QtGui import QFont, QFontDatabase
import wikipediaapi #import Wikipedia
from qgis.gui import QgsMapTool
import re


# wiki_html = wikipedia.ExtractFormat.HTML

# Create a QMessageBox instance
# msgbox = QMessageBox()

# Create a QTextBrowser instance
msgbox = QTextBrowser()

# Set the font size and family
font = QFont("sans-serif", 12)  # font-family: 'Linux Libertine','Georgia','Times',serif;
msgbox.setFont(font)

# Set the width and height
msgbox.setMinimumSize(1080, 800)  # Replace 500 and 400 with your desired width and height

wiki_html = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.HTML
)

def find_total_area(geography):
    # text = "According to the U.S. Census Bureau, the county has a total area of 1,368 square miles (3,540 km2), of which 444 square miles (1,150 km2) is land and 935 square miles (2,420 km2) (67.6%) is water. It is the second-largest county in Illinois by total area and the only one that has more water area than land area. Most of the water is in Lake Michigan."

    text = str(geography)

    # Find the total area
    match = re.search(r"total area of ([\d,]+ square miles)", text)

    if match:
        # Get the total area
        total_area = match.group(1)

        # Bold the total area in the text
        text = text.replace(total_area, f"<b>{total_area}</b>")

    return text

def get_wiki_info(page_name):
    page_html = wiki_html.page(page_name)
    # print_sections(page_html.sections)
    section_summary = page_html.summary
    section_history = page_html.section_by_title('Geography')
    # print(section_summary) 
    # print(section_history.text)
    history_html = find_total_area(section_history)
    print(history_html)
    # print_sections(page_html.sections)
    # return page_html.text
    county_text = '<h2>' + page_name.replace("_"," ") + '</h2><h3>Summary:</h3>' + section_summary + '<br><h3>Geography</h3>' + history_html
    # county_text = '<br><br>'.join([section_summary, section_history.text])  
    return county_text
    # return section_history.text

def show_info_box(page_name):
    wiki_info = get_wiki_info(page_name)
    # msgbox.setTitle(page_name)
    # msgbox.setText(wiki_info)
    # Set the HTML content
    msgbox.setHtml(wiki_info)
    msgbox.show()

def print_sections(sections, level=0):
        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
                print_sections(s.sections, level + 1)



def display_feature(feature, layer):
    show_info_box(feature)
    
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
        # print(point)
        
        # Find the feature at the click location
        for feature in self.layer.getFeatures():
            if feature.geometry().contains(point):
                county_name = f'{feature["NAME"]}_County,_Illinois'
                print("County_Name: ", county_name)
                display_feature(county_name, layer)
                
                # QDesktopServices.openUrl(QUrl(url))
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
