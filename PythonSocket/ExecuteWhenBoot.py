import os, time
stream = 0
stream = os.popen('ffmpeg -r 30 -video_size 640x480 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -c:a aac -ar 44100 -f flv -r 30 rtmp://140.116.202.132:3033/live/UnderWaterVideoKaohsiung')
while True:
  print("stream:")
  print(stream)
  if(stream is not 0)
  {
    stream = os.popen('ffmpeg -r 30 -video_size 640x480 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -c:a aac -ar 44100 -f flv -r 30 rtmp://140.116.202.132:3033/live/UnderWaterVideoKaohsiung')
  }
  #print("There is something wrong, wait for solving")
  #time.sleep(10)
  #stream = os.popen('sudo service webcamd restart')
