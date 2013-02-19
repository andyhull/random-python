from lxml import etree
from geopy import geocoders
import string, fileinput, os, difflib
from xml.sax.saxutils import escape
folder = "/Users/Andy/Documents/work/projects/mapInterface/campusMap/"

def campusGeocode(placename):
    campusPoints = open(folder + 'campusPoints.txt','r')
    pointLocations = campusPoints.readlines()
    campusLocation = ''
    for line in pointLocations:
        location = line.split('|')
        pointName = location[0]
        lng = location[1]
        lat = location[2]
        if placename == pointName:
            campusLocation = "<Point><coordinates>"+str(lng)+","+str(lat)+"</coordinates></Point>"
    return campusLocation
        
        
def addList(value, list):
    if not value in list:
        list.append(value)

logFile = file(folder+'logFile1.txt','w')
logFile.write("id|\n")
newFileX = file(folder+'constructionPhotos3.kml','w')
newFileX.write('<?xml version="1.0" encoding="utf-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Folder><name>Duke Construction Photos</name>')

NSMAP = { 'dc' : "http://purl.org/dc/elements/1.1/",
          'dcterms' : "http://purl.org/dc/terms",
          'duke' : "http://library.duke.edu/metadata/dukecore", 
          'xsi' : "http://www.w3.org/2001/XMLSchema-instance",
          'xlink' : "http://www.w3.org/TR/xlink/" }

dirList=os.listdir("/Users/Andy/Downloads/pp/")
i =0
nameList = []
for fname in dirList:
    if '.xml' in fname:
        filepath = "/Users/Andy/Downloads/pp/"+fname
        root = etree.parse(filepath)
        title = "/mets/dmdSec/mdWrap/xmlData/dc:title"
        # pic = root.xpath("/mets/fileSec/fileGrp[@USE='DEFAULT']/file[@USE='THUMBNAIL']/FLocat[@xlink:href]", namespaces=NSMAP)[0].values()
        #        print pic[0]
        try:
            pic = root.xpath("/mets/fileSec/fileGrp[@USE='DEFAULT']/file[@USE='THUMBNAIL']/FLocat[@xlink:href]", namespaces=NSMAP)[0].values()
            thumbNail = pic[0]
        except IndexError:
            thumbNail = 'none'
        try:
            # use an xpath to extract the "View" (often the building) name
            xpath = "/mets/dmdSec/mdWrap/xmlData/dc:subject[@duke:role='View']"
            view_name = root.xpath(xpath, namespaces = NSMAP)[0].text
            # addList(view_name, nameList)            
            name = root.xpath(title, namespaces = NSMAP)[0].text
            mainUrl = "http://library.duke.edu/digitalcollections/" +root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID") +"/pg.1/"
            print mainUrl
            description = '<![CDATA[<a class="screenshot" href="'+mainUrl+'" target="_blank" rel="'+thumbNail+'"><strong>'+name+'</strong></a>]]>'
            
            kml = "<Placemark><name>"+escape(name)+"</name><description>"+description+"</description>"
            kml +='<ExtendedData><Data name="PlaceName"><value>'+str(view_name)+'</value></Data>'
            kml +='<Data name="MainUrl"><value>'+str(mainUrl)+'</value></Data>'
            kml +='<Data name="Thumb"><value>'+str(thumbNail)+'</value></Data>'
            kml +='<Data name="LayerName"><value>Duke Construction Photos</value></Data>'
            kml +='<Data name="ParentName"><value>'+escape(str(view_name))+'</value></Data></ExtendedData>'
            location = campusGeocode(view_name)
            kml +=location+'</Placemark>'
            newFileX.write(kml)
            print root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID")
        except IndexError:
            # logFile.write(root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID")+"\n")
            print "Sorry, didn't find that path"

newFileX.write('</Folder></Document></kml>')
newFileX.close()
logFile.close()
# use an xpath to extract the place name
# try:
#     xpath = "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Place']"
#     place_name = root.xpath(xpath, namespaces = NSMAP)[0].text
#     print place_name
#     geocodePlace(place_name)
# except IndexError:
#     print "Oops!  That was no valid number.  Try again..."
#     
# 
# # use an xpath to extract the province name
# xpath = "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Province']"
# province_name = root.xpath(xpath, namespaces = NSMAP)[0].text
# if province_name:
#     print province_name
#     geocodePlace(province_name)
# 
# # use an xpath to extract the country name
# xpath = "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Country']"
# country_name = root.xpath(xpath, namespaces = NSMAP)[0].text
# if country_name:
#     print country_name
#     geocodePlace(country_name)

# get place names from a Duke University Progress Photos file
# change to your local path
# filepath = 'x:/xml/mets/duc/pp/ducpp19300702WC0372.xml'
# root = etree.parse(filepath)
# 

