# USV_UnderWaterSensors_Socket
**Data Collection Process(By Raspberry Pi)**
'''
1.Collect weather data, including rain, humidity, luminosity, temperature.  
2.Collect water data.  
3.Schedule the sampling interval.  
4.Record Exception  
5.Send the collected data to the main server.  
'''  
![image](https://user-images.githubusercontent.com/34808088/158133063-885494b1-858e-4689-b37d-f695ff0bfc97.png)

**Power controller to the water chamber (By ESP32)**
'''  
1.Measure the voltage of battery.  
2.Control the sleep and active time of ESP32  
3.Communicate to the Raspberry pi(Server) to change the power schedule and return the voltage measurement.  
4.Control the power of water sensors.  
5.Control the function of pump and valve  
'''  
![image](https://user-images.githubusercontent.com/34808088/158140191-48cf6ae6-e66c-4863-8984-7e82260967a4.png)
