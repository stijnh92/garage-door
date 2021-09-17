#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* SSID = "*";
const char* SSID_PASSWORD = "*";
const char* MQTT_HOST = "*";
const char* MQTT_USER = "*";
const char* MQTT_PASSWORD = "*";
const char* SUB_TOPIC = "home-assistant/garage-door-basement/set";
const char* PUB_TOPIC = "home-assistant/garage-door-basement/sensor";

const int RELAY_PIN = 13;
const int REED_PIN = 2;

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
String strTopic;
int proximity;

void setup_wifi() {
  delay(10);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(SSID);

  WiFi.begin(SSID, SSID_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  strTopic = String((char*)topic);
  if(strTopic == SUB_TOPIC) {
    Serial.println("Toggling garage door...");
    digitalWrite(RELAY_PIN, LOW);
    delay(300);
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("Garage door toggled!");
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient", MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected!");
      // Once connected, publish an announcement...
      client.subscribe(SUB_TOPIC);
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      Serial.println("Try again in 5 seconds...");
      delay(5000);
    }
  }
}

void setup()
{
  Serial.begin(115200);
  setup_wifi();
  client.setServer(MQTT_HOST, 1883);
  client.setCallback(callback);

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(REED_PIN, INPUT_PULLUP);
  digitalWrite(RELAY_PIN, HIGH);

}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;

    int proximity = digitalRead(REED_PIN);
    if (proximity == LOW) {
        Serial.println("Door closed");
        client.publish(PUB_TOPIC, "OFF");
    }
    else {
        Serial.println("Door open");
        client.publish(PUB_TOPIC, "ON");
    }
  }
}
