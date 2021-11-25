import serial, time
from datetime import datetime, timezone, timedelta

def GetRainData():
  # 設定為 +8 時區
  tz = timezone(timedelta(hours=+8))

  # 取得現在時間、指定時區、轉為 ISO 格式
  datetime.now(tz).isoformat()

  ser = serial.Serial()
  ser.port = "/dev/ttyUSB0"

  #9600,N,8,1
  ser.baudrate = 9600
  ser.bytesize = serial.EIGHTBITS #number of bits per bytes
  ser.parity = serial.PARITY_NONE #set parity check
  ser.stopbits = serial.STOPBITS_ONE #number of stop bits
 
  ser.timeout = 0.5          #non-block read 0.5s
  ser.writeTimeout = 0.5     #timeout for write 0.5s
  ser.xonxoff = False    #disable software flow control
  ser.rtscts = False     #disable hardware (RTS/CTS) flow control
  ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
  while(1):
      try: 
          ser.open()        
      except Exception as ex:
          print ("open serial port error " + str(ex))
          exit() 
      if ser.isOpen():
          try:
              ser.flushInput() #flush input buffer
              ser.flushOutput() #flush output buffer  
     
              #listen data per 0.5s
              response = ser.readline()
              if(response):
                  print("read data:")
                  print(str(response))
                  print("Catch time:"+ str(datetime.now(tz).isoformat(timespec="seconds")))
                  return response
     
              ser.close()
              time.sleep(1)
          except Exception as e1:
              print ("communicating error " + str(e1))
     
      else:
          print ("open serial port error")
if __name__ == '__main__':
  RainData = GetRainData()
