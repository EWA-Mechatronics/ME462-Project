/*
 * Middle East Technical University - ME462 Mechatronic Design - 2020
 * Project: Mobile Robot Arena
 *
 * This code allows NodeMCU to connect to an MQTT Broker and controls the robot
 * according to the information received through MQTT subscription.
 * 
 */

#include <PubSubClient.h>  // Required for MQTT communication protocol - https://pubsubclient.knolleary.net/
#include <ESP8266WiFi.h>   // Required for NodeMCU wifi communications - https://arduino-esp8266.readthedocs.io/

int motorA_phase = 15;   // D8 pin - Determines the motor direction
int motorA_enable = 13;  // D7 pin - Determines the motor speed via PWM signal
int motorB_phase = 12;   // D6 pin
int motorB_enable = 14;  // D5 pin
int rgb_R = 16;          // D2 pin - RGB Led R pin
int rgb_G = 5;           // D1 pin - RGB Led G pin
int rgb_B = 4;           // D0 pin - RGB Led B pin
int analogPin = A0;      // A0 ADC pin on Nodemcu - 10-bit resolution

int motorA_direction;    // Define variables to store information about the states the motors
int motorA_speed;
int motorB_direction;
int motorB_speed;

int analogReadOut;                 // Analog pin readout - gives information about the battery level
int battery_percentage;            // Variable to store battery percentage
int battery_interval = 1000;       // Time interval to send battery information via MQTT
unsigned long previousMillis = 0;  // To store the last time battery info was sent
unsigned long currentMillis = 0;   // To store the current time in milliseconds
int critical_battery_level = 30;   // Critical battery level below which the robot stops working
int fade_brightness = 1023;        // For critical battery level indication loop
int fade = 1;                      // For critical battery level indication loop

byte battery_msg[2];               // Message to be sent via MQTT about battery level


/*
 * Confıgure these to suit your setup
 */
const char* mqtt_server = "192.168.1.107";  // Mosquitto broker IP address
const char* ssid = "CANBOLAT_plus";         // Router SSID
const char* password = "canbolat19";        // Router password
const char* publish_topic = "me462_robot_1_battery";       // MQTT topic to publish battery status
const char* subscription_topic = "me462_robot_1_control";  // MQTT topic to subscribe to get control input

WiFiClient esp;  // Creates a client that can connect to a specified IP address and port as defined in client.connect()

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
  digitalWrite(rgb_R, HIGH);  // Make sure that the LED is turned off initially
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
    led_blink('R', 30, 50);  // Blink in red rapidly to indicate lost connection
    connectToWifi();
  }
  if (client.connected() == false)  // Check the mqtt connection & reconnect if the connection is lost
  {
    Serial.println("MQTT connection is lost. Re-connecting...");
    led_blink('R', 30, 50);  // Blink in red rapidly to indicate lost connection
    connectToBroker();
  }

  client.loop();  // This should be called regularly to allow the client to process incoming messages and maintain its connection to the server

  analogReadOut = analogRead(analogPin);                 // Read the analog pin to determine battery level
  battery_percentage = map(analogReadOut,0,1023,0,100);  // These values need to be adjusted for accurate voltage level reading (same below)

  currentMillis = millis();  // Read the current millis and store it
  if (currentMillis - previousMillis > battery_interval)  // Publish the battery information if a certain amount of time has passed
  {
  	previousMillis = currentMillis;
  	battery_msg[0] = battery_percentage;               // Assign battery level info to mqtt message to be sent
  	client.publish(publish_topic, battery_msg, 1);  // Publish the battery information message to the topic "battery_status". (1 byte)
  	Serial.println(battery_percentage);
  }

  // if (battery_percentage < critical_battery_level)     // Critical battery level loop - (???????????????????? Check DEEP SLEEP ?????????????????)
  // {
  // 	Serial.println("WARNING ----- BATTERY LEVEL IS CRITICAL ----- WARNING");
  // 	//Minimize power consumption
  // 	//Make sure that the motors don't draw any current
  // 	while (battery_percentage < critical_battery_level)     // Fading Red LED indicates critical battery level
  // 	{
  //     analogWrite(rgb_R, fade_brightness);
  //     fade_brightness -= fade;
  //     delay(4);
  //     if (fade_brightness < 512 || fade_brightness > 1023)  // Change the direction of fading if the limit is reached
  //     	{
  //     		fade = -fade;
  //     		delay(1000);
  //     	}
  //     analogReadOut = analogRead(analogPin);                 // Read the analog pin to determine battery level again
  //     battery_percentage = map(analogReadOut,0,1023,0,100);  // These values need to be adjusted as above
  // 	}
  //   analogWrite(rgb_R, 1023);  // Turn off the led when the battery is charged enough
  // }

  delay(10);  // Must delay to allow ESP8266 WIFI functions to run ???
}

void connectToWifi()  // The function that establishes the wifi connection
{
  WiFi.begin(ssid, password);
  Serial.print("\nConnecting to ");
  Serial.print(ssid);
  
  while (WiFi.status() != WL_CONNECTED)  // Loop until the wifi connection is established
  {
    led_blink('G', 1, 100);  // Blink in green while trying to connect to wifi
    delay(100);  // Eliminated off time in the function "led_blink" is required here
  }
  Serial.print("\nWiFi connected. ");
  Serial.print("IP address is: ");
  Serial.println(WiFi.localIP());

  led_blink('G', 1, 3000);  // Indicate succesful wifi connection in green for a few seconds
}

void connectToBroker()  // The function that establishes the connection to the MQTT broker
{
  if (WiFi.status() == WL_CONNECTED)  // Check Wifi connection before attemping to connect to MQTT
  {
    while (!client.connected())  // Loop until we're connected to the MQTT server (how to blink here?)
    {
      Serial.print("\nAttempting MQTT connection to ");
      Serial.print(mqtt_server);
      String clientID = "me462_esp8266-"; clientID += String(random(0xffff), HEX);  // Generate a random client ID

      if (client.connect(clientID.c_str()))  // If the connection is successful
      {
        Serial.println("\tMQTT Connected");
        led_blink('B', 1, 3000);               // Indicate succesful MQTT connection in blue for a few seconds
        client.subscribe(subscription_topic);  // Subscribe to the topic
      }
      else
      {
        Serial.print(" ----> FAILED. Re-trying");
        led_blink ('B', 10, 100);  // Blink in blue a few times to indicate mqtt connection failure
        //abort();
      }
    }
  }
  else
  {
    Serial.println("Wifi connection is lost. Re-connecting...");
    led_blink('R', 30, 50);  // Blink in red rapidly to indicate lost connection
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
  motorA_speed = map(motorA_speed,0,99,0,1023);  // The maximum allowable speed of the motors can be set here - 10 bit PWM Resolution
  motorB_speed = map(motorB_speed,0,99,0,1023);
  digitalWrite(motorA_phase, motorA_direction);  // Set the direction of motor A
  digitalWrite(motorB_phase, motorB_direction);  // Set the direction of motor B
  analogWrite(motorA_enable, motorA_speed);      // Set the speed of motor A
  analogWrite(motorB_enable, motorB_speed);      // Set the speed of motor B

  // Serial.println(motorA_direction);
  // Serial.println(motorA_speed);
  // Serial.println(motorB_direction);
  // Serial.println(motorB_speed);
}

void led_analog_control (int r, int g, int b)
{
  analogWrite(rgb_R,1023-r);
  analogWrite(rgb_G,1023-g);
  analogWrite(rgb_B,1023-b);
}

void led_blink (char color, int amount, int interval)
{
	int led;
  switch (color)
  {
    case 'R':
      led = rgb_R;
      break;
    case 'G':
      led = rgb_G;
      break;
    case 'B':
      led = rgb_B;
      break;
  }
  if (amount == 1)  // Eliminate unnecessary off time delay if amount == 1
  {  
    for (int i=0; i<amount; i++)
    {
      digitalWrite(led, LOW);
      delay(interval);
      digitalWrite(led, HIGH);
    }
  }
  else
  {
    for (int i=0; i<amount; i++)
    {
      digitalWrite(led, LOW);
      delay(interval);
      digitalWrite(led, HIGH);
      delay(interval);
    }
  }
}
