import json
import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
#THE_TOPIC  = "$SYS/#"
THE_TOPIC  = "my_sensors/"


# Callback function used when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("connected to ", client._host, "port: ", client._port)
    print("flags: ", flags, "returned code: ", rc)

    # Subscribe to various topics
    client.subscribe(THE_TOPIC + "kitchen", qos=1)
    client.subscribe(THE_TOPIC + "garden", qos=1)
    client.subscribe(THE_TOPIC + "#", qos=1)


# Callback function used when the client receives a message from the broker.
def on_message(client, userdata, msg):
	topic = msg.topic
	payload = msg.payload.decode()

	try:
		data = json.loads(payload)
	# The decodew will fail for messages such as the last will
	except json.JSONDecodeError:
		data = payload

	print("message received with topic: {} and payload: {}".format(topic, data))




# Create the MQTT client object
client = mqtt.Client(client_id="id",
						 clean_session=False,
						 userdata=None, 
						 protocol=mqtt.MQTTv311, 
						 transport="tcp")

# Define basic callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT message broker
client.username_pw_set(username=None, password=None)
client.connect(THE_BROKER, port=1883, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()

