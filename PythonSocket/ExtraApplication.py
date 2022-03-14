# importing geopy library
from geopy.geocoders import Nominatim
import os 
def GetGPSCoordination():
	lat,lon = os.popen('curl ipinfo.io/loc').read().split(',')

	print("Latitude = ", lat, "\n")
	print("Longitude = ", lon)
	return lat, lon
if __name__ == '__main__':
	while(1):  
		#get water information
		GetGPSCoordination()
		#Sleep 1 second
		time.sleep(2)
