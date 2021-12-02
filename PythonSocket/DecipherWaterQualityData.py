"""
*****************************************************************
Project: Unmmaned surface vehicle
File name:DecodeWaterQualityData.py
related file:ReadUnderWaterSensors.py
function:Get data from under water sensors to http server.
author:De-Li
version:1.0
---------------------------------------------------------------
Comment:
2021/11/30
	The "feedback" code for Under water sensors.水質感測設備"應答"碼
        The fourth and fifth number of code mean the reading data.
        AmmoniaNitrogen value has special setting which needs 4-7th code for readind data.
	溶氧值(DissolvedOxygenValue):0x01, 0x03, 0x02, 0x02, 0x01, 0xf8, 0x58
	水溫(Temperature):0x01, 0x03, 0x02, 0x00, 0xc1, 0x79, 0xd4
	水質ORP(WaterQuality):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	濁度(Turbidity):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	氨氮值(AmmoniaNitrogen):0x01, 0x03, 0x04, 0x2c, 0x81, 0x40, 0x91, 0x52, 0xe7
	電導率(Conductivity):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58
	PH值(PHValue):0x01, 0x03, 0x02, 0x02, 0xc1, 0xf8, 0x58	 
---------------------------------------------------------------
Log:
2021/11/30
Create script for Deciphering under water sensors.
---------------------------------------------------------------
"""
import numpy as np
import struct
import codecs

def CombineHexAndDecipher(Num1,Num2):
        Temp_Header = 0x0
        H_Combined = str(Temp_Header)+str(Num1)+str(Num2)
        
        #'!H' means decipher the hex for unsign short
        return struct.unpack('!H', bytes.fromhex(H_Combined))[0]
def CombineHexAndDecipher(Num1,Num2,Num3,Num4):
	#for decipher AmmoniaNitrogen value
        Temp_Header = 0x0
        Temp_Num = np.array([Num3,Num4,Num1,Num2])
        H_Combined = str(Temp_Header)
        for i in range(0,4):
                H_Combined += str(Temp_Num[i])
        
        #'!f' means decipher the hex for float type
        return struct.unpack('!f', bytes.fromhex(H_Combined))[0]
def SplitString(StringArray):        
        for i in range(0,7):
                IterData = codecs.encode(StringArray[i][0],'hex')
                IterData = IterData.decode("utf-8")
                IterData = [IterData[i:i+2] for i in range(0,len(IterData),2)]
                print(IterData)
                if i == 0:
                        SplitedString = np.array(IterData)
                        SplitedString = np.hstack((SplitedString,[0,0]))
                elif i>0 & i!=4:
                        SplitedString = np.vstack((SplitedString,IterData))
                        SplitedString = np.hstack((SplitedString,[0,0]))
                elif i==4:
                        SplitedString = np.vstack((SplitedString,IterData))
        return SplitedString
def DecipherWaterData(RawDataArray):
        #DecipheredData = np.array([['DissolvedOxygenValue'],['Temperature'],['WaterQuality'],['Turbidity'],['AmmoniaNitrogen'],['Conductivity'],['PHValue']])
        SplitedData = SplitString(RawDataArray)                                        
        for i in range(0,7):
                if i==0:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.array((Temp/1000))
                elif i==1:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.hstack((DecipheredData,Temp/10))
                elif i==2:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.hstack((DecipheredData,Temp))
                elif i==3:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.hstack((DecipheredData,Temp))
                elif i==4:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4],SplitedData[i][5],SplitedData[i][6])
                        DecipheredData = np.hstack((DecipheredData,Temp))
                elif i==5:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.hstack((DecipheredData,Temp))
                elif i==6:
                        Temp = CombineHexAndDecipher(SplitedData[i][3],SplitedData[i][4])
                        DecipheredData = np.hstack((DecipheredData,Temp/100))
        print(DecipheredData)
        return DecipheredData
                
                        
                 
        
