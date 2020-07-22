/*
 * This code allows NodeMCU to connect to an MQTT Broker and controls the robot.
 * 
 */

#include <PubSubClient.h>  // Required for MQTT communication protocol - https://pubsubclient.knolleary.net/
#include <ESP8266WiFi.h>   // Required for NodeMCU wifi communications - https://arduino-esp8266.readthedocs.io/

int motorA_phase = 15;   // D8 pin - Determines the motor direction
int motorA_enable = 13;  // D7 pin - Determines the motor speed via PWM signal
int motorB_phase = 12;   // D6 pin
int motorB_enable = 14;  // D5 pin
int rgb_R = 16;   // D2 pin - RGB Led R pin
int rgb_G = 5;   // D1 pin - RGB Led G pin
int rgb_B = 4;  // D0 pin - RGB Led B pin
int analogPin = A0;  // A0 ADC pin on Nodemcu - 10-bit resolution

// Define variables to store information about the states the motors
int motorA_direction;
int motorA_speed;
int motorB_direction;
int motorB_speed;
int analogReadOut;
int battery_percentage;
//int battery_voltage;
int battery_interval;
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
int interval = 3000;
int critical_battery_level = 30;

/*
 * Confıgure these to suit your setup
 */
const char* mqtt_server = "192.168.1.107";  // Mosquitto broker IP address
const char* ssid = "CANBOLAT_plus";   // Router SSID
const char* password = "canbolat19";  // Router password


WiFiClient esp; // Creates a client that can connect to a specified internet IP address and port as defined in client.connect()

void callback(char* topic, byte* payload, unsigned int length);  // (necessary to prevent compiling error)

PubSubClient client(mqtt_server, 1883, callback, esp);  // Creates a fully configured client instance.


void setup()
{
  Serial.begin(115200);  // Start serial communication for debugging purposes

  pinMode(motorA_enable, OUTPUT);
  pinMode(motorA_phase, OUTPUT);
  pinMode(motorB_enable, OUTPUT);
  pinMode(motorB_phase, OUTPUT);
  pinMode(rgb_R, OUTPUT);
  pinMode(rgb_G, OUTPUT);
  pinMode(rgb_B, OUTPUT);
  digitalWrite(rgb_R, HIGH);  // Make sure that the LED turned off initially
  digitalWrite(rgb_G, HIGH);
  digitalWrite(rgb_B, HIGH);

  connectToWifi();    // Run the function that establishes a wifi connection
  connectToBroker();  // Run the function that establishes a connection to MQTT broker/server

  delay(100); // Wait a bit before starting the main loop
}


void loop()  // Main loop
{
  if (WiFi.status() != WL_CONNECTED)  // Check the wifi connection & reconnect if the connection is lost
  {
    Serial.println("Wifi connection is lost. Re-connecting...");
    for (int i=0; i<30; i++)  // Blink in red rapidly (x times) to indicate lost connection
    {
      digitalWrite(rgb_R, LOW);
      delay(50);
      digitalWrite(rgb_R, HIGH);
      delay(50);
    }
    connectToWifi();
  }
  if (client.connected() == false)  // Check the mqtt connection & reconnect if the connection is lost
  {
    Serial.println("MQTT connection is lost. Re-connecting...");
    for (int i=0; i<30; i++)  // Blink in red rapidly (x times) to indicate lost connection
    {
      digitalWrite(rgb_R, LOW);
      delay(50);
      digitalWrite(rgb_R, HIGH);
      delay(50);
    }
    connectToBroker();
  }
  currentMillis = millis();  // Read the current millis and store it

  client.loop();  // This should be called regularly to allow the client to process incoming messages and maintain its connection to the server

  analogReadOut = analogRead(analogPin);  // Read the analog pin to determine battery level
  battery_percentage = map(analogReadOut,0,1023,0,100);  // These values need to be adjusted for accurate voltage level reading <---------------------
  
  if (currentMillis - previousMillis > battery_interval)
  {
  	previousMillis = currentMillis;
  	//Send battery level information
  	Serial.println(battery_percentage);
  }

  if (battery_percentage < critical_battery_level)
  {
  	//LED notification
  }

  delay(10);  // Must delay to allow ESP8266 WIFI functions to run ???
}

void connectToWifi()  // The function that establishes the wifi connection
{
  WiFi.begin(ssid, password);
  Serial.print("\nConnecting to ");
  Serial.print(ssid);
  
  while (WiFi.status() != WL_CONNECTED) // Wait until the wifi connection is established
  {
  	digitalWrite(rgb_G, LOW);  // Blink in green while trying to connect to wifi
    delay(100);
    digitalWrite(rgb_G, HIGH);
    delay(100);
    Serial.print(".");
  }
  Serial.print("\nWiFi connected. ");
  Serial.print("IP address is: ");
  Serial.println(WiFi.localIP());

  digitalWrite(rgb_G, LOW);  // Indicate succesful wifi connection in green for a few seconds
  delay(3000);
  digitalWrite(rgb_G, HIGH);
}

void connectToBroker()  // The function that establishes the connection to the MQTT broker
{
  if (WiFi.status() == WL_CONNECTED)  // Check Wifi connection before attemping to connect to MQTT
  {
    while (!client.connected())  // Loop until we're connected to the MQTT server (how to blink here?) <------------------
    {
      Serial.print("\nAttempting MQTT connection to ");
      Serial.print(mqtt_server);
      String clientID = "me462_esp8266-"; clientID += String(random(0xffff), HEX);  // Generate a random client ID

      if (client.connect(clientID.c_str()))  // If the connection is successful
      {
        Serial.println("\tMQTT Connected");
        digitalWrite(rgb_B, LOW);  // Indicate succesful mqtt connection in blue for a few seconds
        delay(3000);
        digitalWrite(rgb_B, HIGH);
        client.subscribe("topic_name");  // Subscribe to a topic
      }
      else
      {
        Serial.print(" ----> FAILED. Re-trying in 3");
        delay(1000);
        Serial.print("   2");
        delay(1000);
        Serial.println("   1");
        delay(1000);
        //abort();
      }
    }
  }
  else
  {
    Serial.println("Wifi connection is lost. Re-connecting...");
    connectToWifi();
  }
}


/*
 * This function is called when new messages arrive at the client.
 *  - topic (const char[]) - the topic the message arrived on
 *  - payload (byte[]) - the message payload
 *  - length (unsigned int) - the length of the message payload
 */
void callback(char* topic, byte* payload, unsigned int length) // This function is called when new messages arrive at the client.
{
  motorA_direction = payload[0]-48;
  motorB_direction = payload[3]-48;
  motorA_speed = (payload[1]-48)*10 + (payload[2]-48);
  motorB_speed = (payload[4]-48)*10 + (payload[5]-48);
  motorA_speed = map(motorA_speed,0,99,0,255);   // The maximum allowable speed of the motors can be set here
  motorB_speed = map(motorB_speed,0,99,0,255);
  digitalWrite(motorA_phase, motorA_direction);  // Set the direction of motor A
  digitalWrite(motorB_phase, motorB_direction);  // Set the direction of motor B
  analogWrite(motorA_enable, motorA_speed);      // Set the speed of motor A
  analogWrite(motorB_enable, motorB_speed);      // Set the speed of motor B

  digitalWrite(rgb_R,LOW);
  digitalWrite(rgb_G,LOW);
  digitalWrite(rgb_B,LOW);

}
