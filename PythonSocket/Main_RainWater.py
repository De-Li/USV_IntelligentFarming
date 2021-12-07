"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:PostRainData.py
related file: Main_RainWater, PostWaterData.py, PostRainData.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/12/02
The Ip and port of 5936 敬智's computer.
    HOST = '192.168.0.110'
    PORT = 6969
2021/11/30
The Ip and port of 5910 DeLi's computer.
    HOST = '192.168.0.228'
    PORT = 30000
---------------------------------------------------------------
Log:
---------------------------------------------------------------
"""
import threading
import time, urllib2
from PostWaterData import PostWaterData
from PostRainData import PostRainData
def CheckIfInternetIsConnected():
	while(1):
		try:
			urllib2.urlopen('https://tw.yahoo.com/', timeout=5)
			return True
    		except urllib2.URLError as err: 
			pass	

#Declare threading objects
WaterThreading = threading.Thread(target = PostWaterData)
#RainThreading = threading.Thread(target = PostRainData)
while(1):
	CheckIfInternetIsConnected()
	#Engage threading objects
	WaterThreading.start()
	#RainThreading.start()

	WaterThreading.join()
	#RainThreading.join()

	print("Done")
	time.sleep(30)

