"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:DecodeWaterQualityData.py
related file:ReadUnderWaterSensors.py
function:Get data from under water sensors to UDP server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/12/02
1.modifying sequence of sensors and adding the filling array
2.increasing array to string code.

2021/11/30
	The "feedback" code for Under water sensors.水質感測設備"應答"碼
        The fourth and fifth number of code mean the reading data.
        AmmoniaNitrogen value has special setting which needs 4-7th code for readind data.
	溶氧值(DissolvedOxygenValue):0x01, 0x03, 0x02, 0x02, 0x01, 0xf8, 0x58
	水溫(Temperature):0x01, 0x03, 0x02, 0x00, 0xc1, 0x79, 0xd4
	水質ORP(WaterQuality):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	濁度(Turbidity):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	電導率(Conductivity):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	PH值(PHValue):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58	 
	氨氮值(AmmoniaNitrogen):0x01, 0x03, 0x04, 0x2c, 0x81, 0x40, 0x91, 0x52, 0xe7
---------------------------------------------------------------
Log:
2021/11/30
Create script for Deciphering under water sensors.
---------------------------------------------------------------
"""
import numpy as np
import struct
import codecs

def CombineHexAndDecipherTwo(Num1,Num2):
	H_Combined = Num1+Num2
	
	#'!H' means decipher the hex for unsign short, and it convert string to unsign short
	return struct.unpack('!H', bytes.fromhex(H_Combined))[0]
def CombineHexAndDecipherFour(Num1,Num2,Num3,Num4):
	#for decipher AmmoniaNitrogen value
	H_Combined = Num3 + Num4 + Num1 + Num2
	
        #'!f' means decipher the hex for float type, and it convert string to float
	return struct.unpack('!f', bytes.fromhex(H_Combined))[0]
def SplitString(StringArray):        
	try:
		for i in range(0,7):
			#Since the data from sensors are encoded with b'' and \0x, it is mandatory to remove them before analysis.
			#removing \0x from original data.
			IterData = codecs.encode(StringArray[i][0],'hex')
			#removing b''from encoded data.
			IterData = IterData.decode("utf-8")
			#transferring string into array.
			IterData = [IterData[i:i+2] for i in range(0,len(IterData),2)]
			#print(IterData)                
			if i == 0:
				SplitedString = np.array(IterData)
			elif i==6:
				#Due to the incommensurate length of receive data, the filling array help to fill the vacancy.
				filling = np.array([['0','0'],['0','0'],['0','0'],['0','0'],['0','0'],['0','0'],])
				SplitedString = np.hstack((SplitedString, filling))
				SplitedString = np.vstack((SplitedString, IterData))
			elif i>0:
				SplitedString = np.vstack((SplitedString,IterData))			
		return SplitedString
	except:
		print("Waterdata return incomplete!")
def DecipherWaterData(RawDataArray):
        #DecipheredData = np.array([['DissolvedOxygenValue'],['Temperature'],['WaterQuality'],['Turbidity'],['AmmoniaNitrogen'],['Conductivity'],['PHValue']])
	SplitedData = SplitString(RawDataArray)
	print(SplitedData)
	for i in range(0,7):
		if i==0:
			#Input string arguments
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.array((Temp/1000))
		elif i==1:
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.hstack((DecipheredData,Temp/10))
		elif i==2:
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.hstack((DecipheredData,Temp))
		elif i==3:
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.hstack((DecipheredData,Temp))
		elif i==4:
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.hstack((DecipheredData,Temp))
		elif i==5:
			Temp = CombineHexAndDecipherTwo(SplitedData[i][3],SplitedData[i][4])
			DecipheredData = np.hstack((DecipheredData,Temp/100))
		elif i==6:
			Temp = CombineHexAndDecipherFour(SplitedData[i][3],SplitedData[i][4],SplitedData[i][5],SplitedData[i][6])
			DecipheredData = np.hstack((DecipheredData,Temp))			
	#transferring the data array into string type in order to send data easily.
	DecipheredData = '['+', '.join(str(e) for e in DecipheredData)+']'
	#print(DecipheredData)
	return DecipheredData

                
                        
                 
        
