#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>


void setup() {
  // put your setup code here, to run once:
  WiFi.begin("XXXX", "XXXXX");
  int id = 1;
  
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }


  HTTPClient http;
  http.begin("http://IPADDRESS:5000/counter?id=" + String(id));
  int httpCode = http.GET();
  String payload = http.getString();
  Serial.println(httpCode);
  http.end();
  ESP.deepSleep(0);
 
}

void loop() {
}
