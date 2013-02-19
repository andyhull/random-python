from lxml import etree
from geopy import geocoders
import string, fileinput, os
from xml.sax.saxutils import escape

folder = "/Users/Andy/Documents/work/projects/mapInterface/kml/"
# folder = "/Users/Andy/Documents/work/projects/python/data/mapXML/"
# dirList=os.listdir("/Users/Andy/Documents/work/projects/mapInterface/data/xml/")
# for fname in dirList:
#     print fname

logFile = file(folder+'logFile.txt','w')
logFile.write("id|\n")
newFileX = file(folder+'gamble1.kml','w')
newFileX.write('<?xml version="1.0" encoding="utf-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Folder><name>Gamble Photos</name>')

def geocodePlace(placeName):
    # google = geocoders.Google('ABQIAAAAyd8Ez46q598IKMNLNbUO9RTbHIotSlz7z8MSqWC_WMDTAjxWXxQ08mhs95XefmX1qPzksMdiZ4u7NQ')
    #     place, (lat, lng) = google.geocode(placeName, exactly_one=False)
    #     print "\nGoogle Results: %s: %.5f, %.5f" % (place, lat, lng)
    
    gn2 = geocoders.GeoNames2()
    place, (lat, lng) = gn2.geocode(placeName)
    # placeInput = str(place_name)+"|"+str(place)+"|"+str(lat)+"|"+str(lng)+"|\n"
    # placeXML = "<Placemark><name>"+str(place_name)+"</name><description>Hi</description>"
    placeXML = "<Point><coordinates>"+str(lng)+","+str(lat)+"</coordinates></Point>"
    # placeXML += "</Placemark>"
    # newFileX.write(placeXML)
    # newFile.write(placeInput)
    # print "\nGeoNames Results: %s: %.5f, %.5f" % (place, lat, lng)
    return place, lat, lng, placeXML
    
# import xml.etree.cElementTree as etree
NSMAP = { 'dc' : "http://purl.org/dc/elements/1.1/",
          'dcterms' : "http://purl.org/dc/terms",
          'duke' : "http://library.duke.edu/metadata/dukecore", 
          'xsi' : "http://www.w3.org/2001/XMLSchema-instance" }

findPaths = [  "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Place']"]

# findPaths = [  "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Place']",
# "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Province']",
# "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Country']" ]

# get place names from a Gamble METS file
# change to your local path
# filepath = '../data/xml/11A-53.xml'

dirList=os.listdir("/Users/Andy/Downloads/gamble/")
i =0
for fname in dirList:
    # filepath = '../data/xml/27B-276.xml'
    if '.xml' in fname:
        filepath = "/Users/Andy/Downloads/gamble/"+fname
        root = etree.parse(filepath)
        title = "/mets/dmdSec/mdWrap/xmlData/dc:title"
        try:
            # use get() to grab the attribute text from lxml
            thumbNail = root.xpath("/mets/fileSec/fileGrp[@USE='DEFAULT']/file[@USE='THUMBNAIL']/FLocat", namespaces=NSMAP)[0].get("href")
        except IndexError:
            thumbNail = 'none'
            print thumbNail
        # for indPath in findPaths:
            # print "Path = ", indPath
        try:
            xpath = "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Place']"
            place_name = root.xpath(xpath, namespaces = NSMAP)[0].text
            print place_name
            
            name = root.xpath(title, namespaces = NSMAP)[0].text
            mainUrl = "http://library.duke.edu/digitalcollections/" +root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID") +"/"
            description = '<![CDATA[<a class="screenshot" href="'+mainUrl+'" target="_blank" rel="'+thumbNail+'"><strong>'+name+'</strong></a>]]>'
            # print thumbNail
            kml = "<Placemark><name>"+escape(name)+"</name><description>"+description+"</description>"
            kml +='<ExtendedData><Data name="PlaceName"><value>'+str(place_name)+'</value></Data>'
            kml +='<Data name="LayerName"><value>Gamble Photos</value></Data>'
            kml +='<Data name="ParentName"><value>'+escape(str(place_name))+'</value></Data></ExtendedData>'
            test = geocodePlace(place_name)
            kml +=str(test[3])+'</Placemark>'
            newFileX.write(kml)
            print root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID")
            # i = i+1
            # print i
            # print str(test[1])+" , "+str(test[2])
        except IndexError:
            logFile.write(root.xpath("/mets", namespaces = NSMAP)[0].get("OBJID")+"\n")
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
# # use an xpath to extract the campus name
# xpath = "/mets/dmdSec/mdWrap/xmlData/dcterms:spatial[@duke:role='Duke Campus']"
# campus_name = root.xpath(xpath, namespaces = NSMAP)[0].text
# print campus_name
# 
# # use an xpath to extract the "View" (often the building) name
# xpath = "/mets/dmdSec/mdWrap/xmlData/dc:subject[@duke:role='View']"
# view_name = root.xpath(xpath, namespaces = NSMAP)[0].text
# print view_name
