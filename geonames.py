from geopy import geocoders
    
placeName = raw_input("Enter Place:")
google = geocoders.Google('ABQIAAAAyd8Ez46q598IKMNLNbUO9RTbHIotSlz7z8MSqWC_WMDTAjxWXxQ08mhs95XefmX1qPzksMdiZ4u7NQ')
place, (lat, lng) = google.geocode(placeName)
print "\nGoogle Results: %s: %.5f, %.5f" % (place, lat, lng) 

# gn = geocoders.GeoNames()
# print gn.url
# place, (lat, lng) = gn.geocode(placeName, exactly_one=False)
# print "\nGeoNames Results: %s: %.5f, %.5f" % (place, lat, lng)

gn2 = geocoders.GeoNames2()
place, (lat, lng) = gn2.geocode(placeName)
print "\nGeoNames Results: %s: %.5f, %.5f" % (place, lat, lng)