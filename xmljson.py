import json as json
import lxml
from lxml import objectify
import string, fileinput, os
from lxml import etree
import StringIO

class objectJSONEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o, lxml.objectify.IntElement):
            return int(o)
        if isinstance(o, lxml.objectify.NumberElement) or isinstance(o, lxml.objectify.FloatElement):
            return float(o)
        if isinstance(o, lxml.objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return o.__dict__
        return json.JSONEncoder.default(self, o)

folder = "/Users/Andy/Documents/work/projects/mapInterface/testInterface/maptimeline/data/"
newJSON = file(folder + 'construction1.js','w')
newJSON.write("{\n'wikiURL': 'http://code.google.com/p/maptimeline/',\n'wikiSection': 'Timeline example',\n'events' : [\n")
counter=0
tree = objectify.parse("/Users/Andy/Documents/work/projects/mapInterface/testInterface/maptimeline/data/construction_timeline2.xml")
obj = etree.tostring(tree)
root = objectify.fromstring(obj)

for el in root.event:
    counter = counter+1
    if counter >= 2:
        newJSON.write("},\n")
    newJSON.write("{'id':'"+str(counter)+"',\n")
    if el.get("start"):
        newJSON.write("'start':'"+el.get("start")+"',\n")
    if el.get("end"):
        newJSON.write("'end':'"+el.get("end")+"',\n")
    newJSON.write("'lat': 36.001053341605704,\n")
    newJSON.write("'lon': -78.938112809300662,\n")
    if el.get("title"):
        newJSON.write("'title': '"+el.get("title").replace('\n','')+"'")
    if el.text:
        newJSON.write(",\n'description': '"+el.text.replace('\n','')+"'")
    if el.img.get("src"):
        newJSON.write(",\n'img':'"+el.img.get("src")+"'\n")
newJSON.write("}\n]\n}")
newJSON.close