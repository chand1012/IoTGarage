#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char* ssid = "";
const char* password = "";
IPAddress host(192, 168, 1, 2);
const int ledPin = 8; // this will change
const int sensorPin = 2;

unsigned long timeout = 0;

int val = LOW;

WifiClient client;

void setup() {
    Serial.begin(9600);
    Serial.println();
    pinMode(ledPin, OUTPUT);
    pinMode(sensorPin, INPUT);
    Serial.printf("Connecting to %s", ssid);
    Wifi.begin(ssid, password);
    while (Wifi.status != WL_CONNECTED) {
        delay(500);
        Serial.println(".")
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
            if (client.connect(host, 55555)) {
                client.print(String("GET /motionSensor/webhook") + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n");
                while (client.connected() || client.available()){
                    if (client.available()) {
                        String line = client.readStringUntil("\n");
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