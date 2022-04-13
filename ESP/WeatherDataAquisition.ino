#include <Arduino.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h> //引用以使用UDP
#include <Adafruit_I2CDevice.h>
#include "Adafruit_SHT31.h"
#include <DFRobot_B_LUX_V30B.h>
#include "user_interface.h"


//------sensors------
#define TempHumidity 0x44

// LUX declaration
DFRobot_B_LUX_V30B    myLux(13, 14, 12); //The sensor chip is set to 13 pins(No need to change), SCL(14) and SDA(12) adopt default configuration. The pin of SCL and SDA can be change if needed.

// SHT31 Declaration
const char* ssid = "5910";
const char* password = "0933664603";
Adafruit_SHT31 sht31 = Adafruit_SHT31();                                
WiFiUDP Udp;                      //建立UDP物件
const char* IP = "192.168.1.102";
unsigned int ServerUdpPort = 6060;
//unsigned int localUdpPort = 5555; //本地埠號

void ConnectWiFi()
{
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.print("");
  Serial.println("WiFi connected");
  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());
}

void setup()
{
  Serial.begin(115200);
  myLux.begin();
  sht31.begin(TempHumidity);
  ConnectWiFi();
  WiFi.mode(WIFI_STA);
  // the below instructions and now u will receive.
  wifi_set_sleep_type(NONE_SLEEP_T); //LIGHT_SLEEP_T and MODE_SLEEP_T
}

void SendingData(float temperature, float humidity, float Lux)
{
  int Size;
  char sending[50];
  char T[9];
  char H[9];
  char L[9];
  dtostrf(temperature, 6, 2, T);
  dtostrf(humidity, 6, 2, H);
  dtostrf(Lux, 7, 1, L);
  if(Lux < 100.0)
  {
    Size = 22;
  }
  else if(Lux>100000.0)
  {
    Size = 26;
  }
  else if(Lux>10000.0)
  {
    Size = 25;
  }
  else if(Lux>1000.0)
  {
    Size = 24;
  }
  else
  {
    Size = 23;
  }
  sprintf(sending,"%s, %s, %s", T, H, L);
  Udp.beginPacket(IP, ServerUdpPort);
  Udp.write((const uint8_t*)sending, Size);
  Udp.endPacket();
  Serial.print("sending string:" );
  Serial.println(sending);
}

void loop()
{
  //SHT31
  float t = sht31.readTemperature();
  float h = sht31.readHumidity();
  float Lux = myLux.lightStrengthLux();
  SendingData(t,h,Lux);
  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());
  delay(5000);
  
}
