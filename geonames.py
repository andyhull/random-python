from geopy import geocoders
    
placeName = raw_input("Enter Place:")
google = geocoders.Google('your_key')
place, (lat, lng) = google.geocode(placeName)
print "\nGoogle Results: %s: %.5f, %.5f" % (place, lat, lng) 

# gn = geocoders.GeoNames()
# print gn.url
# place, (lat, lng) = gn.geocode(placeName, exactly_one=False)
# print "\nGeoNames Results: %s: %.5f, %.5f" % (place, lat, lng)

gn2 = geocoders.GeoNames2()
place, (lat, lng) = gn2.geocode(placeName)
print "\nGeoNames Results: %s: %.5f, %.5f" % (place, lat, lng)