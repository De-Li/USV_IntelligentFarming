#include <WiFi.h>
#include <esp_sleep.h>

//#include <ESP8266WiFi.h>
#include<NTPClient.h>
//#include<WiFiUdp.h>

const char *ssid = "5910";
const char *password = "0933664603";
WiFiServer server(100);
int n = 0;


//Voltage measurement parameters
int ANALOG_IN_PIN = A0;
float Vout = 0.0;
float Vin = 0.0;
float R1 = 30000.0;
float R2 = 13800;
int value = 0;

//NTP TIME
String TimeData;
int GMT = 8;
String hours ;
String minutes;
String seconds;
String times;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
unsigned long ValveStartTime;
unsigned long ValveCurrentTime;
unsigned long ESPStartTime;
unsigned long ESPCurrentTime;

//RELAY
String relayLOW_time, relayHIGH_time, pump_in_time, pump_out_time, Schedule_Return;
String Schedule[5];
String  LowTime, MidTime;
int relay_valve = 0;
//int relay_pump_in  ;
int relay_Sensor ;

// Schedule
int Position[8];
String NewString, myString;
String  Schedule_message;
int myString_length;
float High_Voltage, Low_Voltage;
float ExecutiveSchedule[5] = {12, 300, 1500, 180, 60};
bool FlagOfValve = false;
//ExecutiveSchedule[0]低電壓
//ExecutiveSchedule[1]執行時間
//ExecutiveSchedule[2]睡眠時間
//ExecutiveSchedule[3]水存放在桶子內的時間長度
//ExecutiveSchedule[4]水閥開啟的時間長度


float c, d;
String Volt1, Volt2;

//判斷電瓶電壓大小
float GetVoltage()
{
  value = analogRead(ANALOG_IN_PIN);
  Vout = (value * 5.0) / 1023.0;
  //Serial.println(Vout);
  //Serial.println(Vout*3.18388429752);
  Vin = Vout / (R2 / (R1 + R2));
  //Serial.println(Vin);
  return Vin;
}

//判斷電瓶電壓範圍，執行時間及睡眠時間
int CheckBatteryStatus()
{
  if (GetVoltage() > 12)//中電量
  {
    //esp_sleep_enable_timer_wakeup(ExecutiveSchedule[2]*1000000);
    digitalWrite(relay_Sensor, HIGH);
    Serial.print("目前電壓:"); Serial.println(Vin);
    //delay(ExecutiveSchedule[1] * 1000);
    Serial.println("Battery is Mid!");
    //esp_deep_sleep_start();
    return 1;
  }
  else if (GetVoltage() < 12)//低電量
  {
    //esp_sleep_enable_timer_wakeup(1740*1000000);
    digitalWrite(relay_Sensor, HIGH);
    Serial.print("目前電壓:"); Serial.println(Vin);
    Serial.println("Battery is LOW!");
    return 0;
  }
}

//分析由樹莓派傳來的字串內容
void SetSchedule(String myString)
{
  String comma = ",";
  Volt2 = String(GetVoltage());
  if (myString == "ShowStatus")
  {
    Serial.print("ShowStatus!");

    //String Schedule_Size = Schedule[0]+Schedule[1]+Schedule[2]+Schedule[3]+Schedule[4]+comma+comma+comma+comma;
    Schedule_Return = Volt2 + comma + String(ExecutiveSchedule[0]) + comma + String(ExecutiveSchedule[1]) + comma + String(ExecutiveSchedule[2]) + comma + String(ExecutiveSchedule[3]) + comma + String(ExecutiveSchedule[4]);
    Serial.print(Schedule_Return);
    return;
  }
  else
  {
    Position[0] = myString.indexOf(',');
    Serial.println("Position[0]");
    Serial.println(Position[0]);
    if (Position[0] == -1 || myString.length() <= 18)
    {
      Serial.println("Didn't find the comma!");
      ExecutiveSchedule[0] = 12;
      ExecutiveSchedule[1] = 300;
      ExecutiveSchedule[2] = 1500;
      ExecutiveSchedule[3] = 180;
      ExecutiveSchedule[4] = 60;
      Schedule_Return = Volt2 + comma + String(ExecutiveSchedule[0]) + comma + String(ExecutiveSchedule[1]) + comma + String(ExecutiveSchedule[2]) + comma + String(ExecutiveSchedule[3]) + comma + String(ExecutiveSchedule[4]);
      return;
    }
  }
  Position[0] = myString.indexOf(','); //找出第一個逗點的位置並存放在Position1
  for (int n = 0; n < 4; n++)
  {
    Position[n + 1] = myString.indexOf(',', Position[n] + 1);
  }
  NewString = myString.substring(0, Position[0]); //0~1可顯示0的數字
  ExecutiveSchedule[0] = NewString.toDouble();

  NewString = myString.substring(Position[0] + 1, Position[1]);
  ExecutiveSchedule[1] = NewString.toDouble();

  NewString = myString.substring(Position[1] + 1, Position[2]);
  ExecutiveSchedule[2] = NewString.toDouble();

  NewString = myString.substring(Position[2] + 1, Position[3]);
  ExecutiveSchedule[3] = NewString.toDouble();

  NewString = myString.substring(Position[3] + 1, Position[4]);
  ExecutiveSchedule[4] = NewString.toDouble();
  Schedule_Return = Volt2 + comma + String(ExecutiveSchedule[0]) + comma + String(ExecutiveSchedule[1]) + comma + String(ExecutiveSchedule[2]) + comma + String(ExecutiveSchedule[3]) + comma + String(ExecutiveSchedule[4]);
  return;
}

//水閥在指定的時間打開
void valve()
{
  ValveCurrentTime = millis();
  timeClient.update();
  hours = String(timeClient.getHours() + GMT);
  minutes = String(timeClient.getMinutes());
  seconds = String(timeClient.getSeconds());
  if (FlagOfValve == false)
  {
    if (minutes == "4" || minutes == "39")
    {
      pump_out_time = hours + ":" + minutes + ":" + seconds;
      ValveStartTime = millis();
      digitalWrite(relay_valve, LOW); //設常開，LOW時水閥放水
      Serial.print("閥門開啟時TIME:"); Serial.println(pump_out_time);
      //delay(ExecutiveSchedule[4]);//水閥開啟的時間
      FlagOfValve = true;
    }
  }
  else if (ValveCurrentTime - ValveStartTime > ExecutiveSchedule[4] * 1000 && FlagOfValve == true)
  {
    Serial.println("Valve is close!");
    digitalWrite(relay_valve, HIGH);
    FlagOfValve = false;
  }
  Serial.println("Valve Time");
  Serial.println(ValveCurrentTime - ValveStartTime);
  //delay(ExecutiveSchedule[3]); //水放置水桶內時間
}

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  pinMode(relay_valve, OUTPUT);
  pinMode(relay_Sensor, OUTPUT);
  digitalWrite(relay_Sensor, LOW);
  valve();
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
    n++;
    Serial.print(n);
    timeClient.begin();
    server.begin();
    Serial.println("Server started");
    //判斷WIFI未連接時，則跳出檢查
    if (n > 20)
      break;
  }
  timeClient.update();
  hours = String(timeClient.getHours() + GMT);
  minutes = String(timeClient.getMinutes());
  seconds = String(timeClient.getSeconds());
  Serial.println("Connected");
  Serial.print("IP Address:"); Serial.println(WiFi.localIP());
  ESPStartTime = millis();
}

void loop() {
  ESPCurrentTime = millis();
  unsigned long ListeningStartTime = millis();
  valve();
  Serial.println("loop!!");
  WiFiClient client = server.available();
  if (client) {  //if get new client
    while (client.connected())
    {
      unsigned long ListeningCurrentTime = millis();
      Serial.print("Connected!");
      //Serial.print("new client");
      //Serial.println(WiFi.localIP());
      if (client.available() > 0)
      {
        String myString = client.readString();
        Serial.println(myString);
        //client.print("Received!!");
        SetSchedule(myString);
        client.print(Schedule_Return);
        break;
      }
      if (ListeningCurrentTime - ListeningStartTime > 5000)
      {
        break;
      }
      delay(500);
    }
  }
  Serial.println(ExecutiveSchedule[0]);
  Serial.println(ExecutiveSchedule[1]);
  Serial.println(ExecutiveSchedule[2]);
  Serial.println(ExecutiveSchedule[3]);
  Serial.println(ExecutiveSchedule[4]);
  bool BatteryStatus = CheckBatteryStatus();
  if (BatteryStatus == 0 && ESPCurrentTime - ESPStartTime > ExecutiveSchedule[1] * 1000)
  {
    digitalWrite(relay_Sensor, HIGH);//繼電器常開
    digitalWrite(relay_valve, HIGH);//繼電器長開
    Serial.println("Sleep");
    esp_sleep_enable_timer_wakeup(ExecutiveSchedule[2] * 1000000);
  }
  else if (ESPCurrentTime - ESPStartTime > ExecutiveSchedule[1] * 1000)
  {
    digitalWrite(relay_Sensor, HIGH);
    digitalWrite(relay_valve, HIGH);
    Serial.println("Sleep");
    esp_sleep_enable_timer_wakeup(ExecutiveSchedule[2] * 1000000);
  }
  Serial.println("ESPCurrentTime - ESPStartTime");
  Serial.println(ESPCurrentTime - ESPStartTime);
  delay(1000);
}
