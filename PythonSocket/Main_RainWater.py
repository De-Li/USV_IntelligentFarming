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
import time
from PostWaterData import PostWaterData
from PostRainData import PostRainData

#Declare threading objects
WaterThreading = threading.Thread(target = PostWaterData)
RainThreading = threading.Thread(target = PostRainData)

#Engage threading objects
WaterThreading.start()
RainThreading.start()

WaterThreading.join()
RainThreading.join()

print("Done")
t.sleep(30)

