#include <ESP8266WiFi.h>

const int doortrig = 1023;
const int lighttrig = 512;

const char *ssid = "";     
const char *password = ""; 

const int trigPin = 0; // D3
const int echoPin = 4; // D2
String output = "";
String dist;
long duration;
int distance;
int doorpin = 2;
WiFiServer server(80);

void setup()
{
  Serial.begin(115200);
  delay(10);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(doorpin, OUTPUT);
  digitalWrite(doorpin, LOW);
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

void uDist()
{
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  distance= duration*0.034/2;
}

void toggleGarage()
{
  analogWrite(doorpin, doortrig);
  delay(350);
  analogWrite(doorpin, doortrig);
}

void toggleGarageLight() 
{
  analogWrite(doorpin, lighttrig);
  delay(350);
  analogWrite(doorpin, lighttrig);
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

  if (request.indexOf("/toggleGarage") != -1)
  {
    toggleGarage();
    output = "";
  } else if (request.indexOf("/getGarage") != -1) {
    uDist();
    dist = String(distance);
    if (distance >= 10){
      output = "<h1>Garage door is closed.</h1>";
    } else {
      output = "<h1>Garage door is open.</h1>";
    }
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println(output);
  client.println("\n");
  client.println("<p>Distance from sensor: " + dist + "</p>");
  client.println("</html>");

  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
}
