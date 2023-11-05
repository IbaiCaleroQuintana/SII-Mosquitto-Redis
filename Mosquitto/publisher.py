import random
import time
import json
import paho.mqtt.client as mqtt


THE_BROKER = "test.mosquitto.org"
THE_TOPIC  = "my_sensors/"


# In a real deployment this should retrieve the actual data from the sensors
def obtain_temperature():
    return random.randint(20, 30)

# Callback function used when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("connected to ", client._host, "port: ", client._port)
    print("flags: ", flags, "returned code: ", rc)

# Callback function used when a message is published.
def on_publish(client, userdata, mid):
    print("msg published (mid={})".format(mid))



# Create the MQTT client object
client = mqtt.Client(client_id="",
					clean_session=True,
					userdata=None,
					protocol=mqtt.MQTTv311,
					transport="tcp")

# Set Last Will and Testament. This message will be sent if the publisher disconnects unexpectedly
client.will_set(THE_TOPIC, payload="The publisher likely crashed", qos=1, retain=False)


# Define basic callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT message broker
client.username_pw_set(username=None, password=None)
client.connect(THE_BROKER, port=1883, keepalive=60)

'''
Retained message: if the flag retain is set to True when sending a message it will be a retained message.
For every channel the broker will remember the last retained message. Every time a client connects to a channel
the broker will send him the last retained message

#msg_to_be_sent = "This is the retained message. Welcome to the channel"
#client.publish(THE_TOPIC,
#			payload=msg_to_be_sent,
#			qos=0,
#			retain=True)
'''
while True:
	print("Publishing messages...")

	temperature_kitchen = obtain_temperature()
	data = {
		"TEMP": temperature_kitchen
	}
	message = json.dumps(data)
	# Publish the message with QoS 1 (at least 1 delivery)
	client.publish(THE_TOPIC + "kitchen",
				payload=message,
				qos=1,
				retain=False)


	temperature_garden = obtain_temperature()
	data = {
		"TEMP": temperature_garden
	}
	client.publish(THE_TOPIC + "garden",
				payload=message,
				qos=1,
				retain=False)

	time.sleep(5)


