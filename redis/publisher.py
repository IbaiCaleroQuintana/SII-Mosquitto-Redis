import redis
import time
import random
import json

def obtain_temperature():
    return random.randint(20, 30)



channel_name = "sensors/"

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

while 1:
    # Measure data to be published
    temperature_kitchen = obtain_temperature()
    # Encode it in json
    data = {
        "TEMP": temperature_kitchen,
    }
    message = json.dumps(data)
    # Send it to the Redis broker
    r.publish(channel_name + "kitchen", message)


    temperature_garden = obtain_temperature()
    data = {
        "TEMP": temperature_garden,
    }
    message = json.dumps(data)
    r.publish(channel_name + "garden", message)

    print("Sleeping 5 seconds before publishing again")
    time.sleep(5)

