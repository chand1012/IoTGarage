#include <ESP8266WiFi.h>

const char *ssid = "";     
const char *password = ""; 

int lampState = 0;
const int lampPin = 2;
WiFiServer server(80);

void setup()
{
  Serial.begin(115200);
  delay(10);
  pinMode(lampPin, OUTPUT);
  digitalWrite(lampPin, lampState);
  // Connect to WiFi network

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP()); //Gets the WiFi shield's IP address and Print the IP address of serial monitor
  Serial.println("/");
}

void toggleLamp(){
    if (lampState==0){
        lampState = 1;
    } else {
        lampState = 0;
    }
    digitalWrite(lampPin, lampState);
}

void loop()
{
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }

  // Wait until the client sends some data
  Serial.println("new client");
  while (!client.available())
  {
    delay(1);
  }

  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Match the request

  if (request.indexOf("/lampSwitch") != -1)
 {
    toggleLamp();
 }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");

  client.println("</html>");

  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
}
