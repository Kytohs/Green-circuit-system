import paho.mqtt.client as mqtt
from utils.mqtt_client import connect_mqtt
import requests

API_URL = "http://127.0.0.1:5000/update-bin"

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    bin_id, weight, location = payload.split(",")

    # Send data to Flask API
    requests.post(API_URL, json={"bin_id": bin_id, "weight": int(weight), "location": location})
    print(f"Data sent: Bin {bin_id} - {weight}% full at {location}")

mqtt_broker = "broker.hivemq.com"
client = mqtt.Client("SmartBin123")
client.connect(mqtt_broker, 1883)

client.subscribe("ewaste/bins")
client.on_message = on_message

client.loop_forever()
