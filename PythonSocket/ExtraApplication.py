# importing geopy library
from geopy.geocoders import Nominatim
import os 

lat,lon = os.popen('curl ipinfo.io/loc').read().split(',')

print("Latitude = ", lat, "\n")
print("Longitude = ", lon)
