#include <WiFi.h>
#include <esp_sleep.h>
#include<NTPClient.h>

//---------------parameters------------------
const char *ssid = "5910";
const char *password = "0933664603";
WiFiServer server(100);

//Voltage measurement parameters
int ANALOG_IN_PIN = 36;
int value = 0;
float Vin = 0.0;

//NTP TIME
int GMT = 8;
String TimeData, hours, minutes, seconds, times;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

//RELAY
int relay_valve = 17;
int relay_Sensor = 16;

// Schedule
int Position[8];
String RecievedMessage, Schedule_Return;
//電壓閾值, 睡眠時間點, 睡眠時長, 水閥開啟時間點, 水閥關閉時間點, Loop的delay時間
RTC_DATA_ATTR String ExecutiveSchedule[6] = {"12", "6", "1380", "5", "6", "2000"};
bool FlagOfValve = false;
int VoltageReadingSum = 0;
int DelayTimePerLoop = ExecutiveSchedule[5].toInt();

//-----------------------Function--------------------------
//判斷電瓶電壓大小
float GetVoltage()
{
  for (int i = 0; i < 8 ; i++)
  {
    value = analogRead(ANALOG_IN_PIN);
    VoltageReadingSum += value;
    delay(200);
  }
  Vin = (VoltageReadingSum / 8) / 243.0;
  Serial.print("目前電壓:");
  Serial.println(Vin);
  VoltageReadingSum = 0;
  return Vin;
}

//判斷電瓶電壓範圍，執行時間及睡眠時間
int ControlPowerOfSensors()
{
  GetVoltage();
  if (Vin >= ExecutiveSchedule[0].toInt())//中電量
  {
    digitalWrite(relay_Sensor, HIGH);
    Serial.println("Battery is sufficient, Turn on the sensors!");
    return 1;
  }
  else if (Vin < ExecutiveSchedule[0].toInt())//低電量
  {
    digitalWrite(relay_Sensor, LOW);
    Serial.println("Battery is lean, Keep the sensors off!");
    return 0;
  }
}

//分析由樹莓派傳來的字串內容
void ParseMessage(String RecievedMessage)
{
  String comma = ",";
  Schedule_Return = String(Vin);
  if (RecievedMessage == "ShowStatus")
  {
    Serial.print("Message from RPI is ShowStatus!");
    for (int i = 0; i < 6; i++)
    {
      Schedule_Return += comma;
      Schedule_Return += String(ExecutiveSchedule[i]);
    }
    //Schedule_Return = String(Vin) + comma + String(ExecutiveSchedule[0]) + comma + String(ExecutiveSchedule[1]) + comma + String(ExecutiveSchedule[2]) + comma + String(ExecutiveSchedule[3]) + comma + String(ExecutiveSchedule[4]);
    Serial.print(Schedule_Return);
    return;
  }
  else
  {
    Position[0] = RecievedMessage.indexOf(',');
    if (Position[0] == -1 || RecievedMessage.length() <= 18)
    {
      Serial.println("The format of message is wrong!");
      ExecutiveSchedule[0] = "12";
      ExecutiveSchedule[1] = "6";
      ExecutiveSchedule[2] = "1380";
      ExecutiveSchedule[3] = "5";
      ExecutiveSchedule[4] = "6";
      ExecutiveSchedule[5] = "2000";
      for (int i = 0; i < 6; i++)
      {
        Schedule_Return += comma;
        Schedule_Return += String(ExecutiveSchedule[i]);
      }
      //Schedule_Return = String(Vin)+ comma + ExecutiveSchedule[0] + comma + ExecutiveSchedule[1] + comma + ExecutiveSchedule[2] + comma + ExecutiveSchedule[3] + comma + ExecutiveSchedule[4];
      return;
    }
  }
  Position[0] = RecievedMessage.indexOf(','); //找出第一個逗點的位置並存放在Position1
  for (int n = 0; n < 5; n++)
  {
    Position[n + 1] = RecievedMessage.indexOf(',', Position[n] + 1);
  }
  ExecutiveSchedule[0] = RecievedMessage.substring(0, Position[0]); //0~1可顯示0的數字
  for (int i = 1; i < 6 ; i++)
  {
    ExecutiveSchedule[i] = RecievedMessage.substring(Position[i - 1] + 1, Position[i]);
  }
  for (int i = 0; i < 6; i++)
  {
    Schedule_Return += comma;
    Schedule_Return += String(ExecutiveSchedule[i]);
  }
  return;
}

//水閥在指定的時間打開
void valve()
{
  timeClient.update();
  hours = String(timeClient.getHours() + GMT);
  minutes = String(timeClient.getMinutes());
  seconds = String(timeClient.getSeconds());
  //int minutes_1= minutes.toInt();
  if (FlagOfValve == false)
  {
    if (minutes == ExecutiveSchedule[3])
    {
      String pump_out_time;
      pump_out_time = hours + ":" + minutes + ":" + seconds;
      digitalWrite(relay_valve, HIGH); //設常開，LOW時水閥放水
      Serial.print("閥門開啟時TIME:"); 
      Serial.println(pump_out_time);
      FlagOfValve = true;
    }
  }
  else if (minutes == ExecutiveSchedule[4] && FlagOfValve == true)
  {
    Serial.println("Valve is close!");
    digitalWrite(relay_valve, LOW);
    //FlagOfValve = false;
  }
}

//------------------------main---------------------------
void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  pinMode(relay_valve, OUTPUT);
  pinMode(relay_Sensor, OUTPUT);
  digitalWrite(relay_Sensor, LOW);
  digitalWrite(relay_valve, LOW);
  int WifiTryCount =0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
    WifiTryCount++;
    Serial.print(WifiTryCount);
    timeClient.begin();
    server.begin();
    Serial.println("Server started");
    //判斷WIFI未連接時，則跳出檢查
    if (WifiTryCount > 20)
      break;
  }
  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.println("Connected");
    Serial.print("IP Address:");
    Serial.println(WiFi.localIP());
  }
  else
  {
    Serial.println("Not Connected");
  }
  timeClient.update();
  hours = String(timeClient.getHours() + GMT);
  minutes = String(timeClient.getMinutes());
  seconds = String(timeClient.getSeconds());
  ControlPowerOfSensors();
  esp_sleep_enable_timer_wakeup(ExecutiveSchedule[2].toInt() * 1000000);
}

void loop() {
  unsigned long Acc_Time = millis();
  timeClient.update();
  hours = String(timeClient.getHours() + GMT);
  minutes = String(timeClient.getMinutes());
  seconds = String(timeClient.getSeconds());
  unsigned long ListeningStartTime = millis();
  valve();
  WiFiClient client = server.available();
  if (client) {  //if get new client
    while (client.connected())
    {
      unsigned long ListeningCurrentTime = millis();
      Serial.print("Connected!");
      Serial.print("new client");
      Serial.println(WiFi.localIP());
      if (client.available() > 0)
      {
        String RecievedMessage = client.readString();
        Serial.println(RecievedMessage);
        ParseMessage(RecievedMessage);
        client.print(Schedule_Return);
        if(FlagOfBattery == false)
        {
          client.print("BatteryLean");
        }
        break;
      }
      if (ListeningCurrentTime - ListeningStartTime > 5000)
      {
        Serial.print("break due to time limit");
        break;
      }
      delay(500);
    }
  }
  if (minutes == ExecutiveSchedule[1])
  {
    digitalWrite(relay_Sensor, LOW);//繼電器常開
    digitalWrite(relay_valve, LOW);//繼電器長開
    Serial.println("Sleep by Time point");
    esp_deep_sleep_start();
  }
  //if ESP32 doesn't sleep when the time point meet, then force it to sleep.
  //The threshold of time limit should be the sampling cycle, for example, 60 mins for now.
  else if (FlagOfValve == true && Acc_Time > 6000000)
  {
    digitalWrite(relay_Sensor, LOW);//繼電器常開
    digitalWrite(relay_valve, LOW);//繼電器長開
    Serial.println("Sleep by Timer");
    esp_deep_sleep_start();
  }
  Serial.println("Accumulate time");
  Serial.println(Acc_Time);
  delay(DelayTimePerLoop);
}
