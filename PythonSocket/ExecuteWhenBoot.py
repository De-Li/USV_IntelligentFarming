import os, time
#while True:
stream = os.popen('ffmpeg -r 10 -re -i http://192.168.1.129/webcam/?action=stream -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -ar 44100 -f flv -r 10 rtmp://140.116.202.132:3033/live/UnderWaterVideoKaohsiung')
  #print("There is something wrong, wait for solving")
  #time.sleep(10)
  #stream = os.popen('sudo service webcamd restart')
