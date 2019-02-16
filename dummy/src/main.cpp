#include <Arduino.h>

unsigned long last = 0;

void setup()
{
  Serial.begin(115200);
};


void printInfo() {
  Serial.print(F("Free heap: "));
  Serial.println(ESP.getFreeHeap());
  Serial.print(F("Sketch size: "));
  Serial.println(ESP.getSketchSize());
  Serial.print(F("Free sketch space: "));
  Serial.println(ESP.getFreeSketchSpace());
  Serial.print(F("SDK Version: "));
  Serial.println(ESP.getSdkVersion());
  Serial.print(F("Flash chip size: "));
  Serial.println(ESP.getFlashChipSize());
  Serial.print(F("Flash chip speed: "));
  Serial.println(ESP.getFlashChipSpeed());
#ifdef ESP32
  Serial.print(F("Min free heap: "));
  Serial.println(ESP.getMinFreeHeap());
  Serial.print(F("Max alloc heap: "));
  Serial.println(ESP.getMaxAllocHeap());
  Serial.print(F("PSRAM size: "));
  Serial.println(ESP.getPsramSize());
  Serial.print(F("Chip revision: "));
  Serial.println(ESP.getChipRevision());
#endif
};

void loop() {
  unsigned long now = millis();

  if (now - last > 2000) {
#ifdef ESP32
    Serial.println(F("Hello ESP32!"));
#endif
#ifdef ESP8266
    Serial.println(F("Hello ESP8266!"));
#endif
    printInfo();
    last = now;
  };

};
