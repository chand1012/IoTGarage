#include <ESP8266WiFi.h>
// this is on a webmos uno-style ESP8266
// so my PIR sensor is fucked so this is unused for now
// also the webmos is being fucky about this code specifically
const char* ssid = "";
const char* password = "";
//IPAddress host(192, 168, 1, 2);
const char* host = "http://192.168.1.29";
const int ledPin = 11; // this will change
const int sensorPin = 0;
unsigned long timeout = 0;
char newline = '\n';
int val = LOW;

void setup() {
    Serial.begin(115200);
    Serial.println();
    pinMode(ledPin, OUTPUT);
    pinMode(sensorPin, INPUT);
    Serial.printf("Connecting to %s", ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println(".");
    }
    Serial.println("Connected");
}

void loop() {
    val = digitalRead(sensorPin);
    if (val == HIGH) {
        digitalWrite(ledPin, HIGH);
        if (timeout <= millis()) {
            timeout = millis() + 5000;
            Serial.printf("Sending request to server...");
            WiFiClient client;
            if (client.connect(host, 55555)) {
                client.print(String("GET /motionSensor/webhook") + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n");
                while (client.connected() || client.available()){
                    if (client.available()) {
                        String line = client.readStringUntil(newline);
                        Serial.println(line);
                    }
                }
                client.stop();
                Serial.printf("Connection ended.");
            }
        }
    } else {
        digitalWrite(ledPin, LOW);
    }
}
