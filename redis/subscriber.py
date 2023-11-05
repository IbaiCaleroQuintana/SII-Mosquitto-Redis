import redis
import json

def handle_msg(msg):
    if msg['type'] == 'message' or msg['type'] == "pmessage":
        if msg['type'] == "pmessage":
            print("MESSAGE HANDLER: " + msg['channel'].decode('utf-8') + " pattern: " + msg['pattern'].decode('utf-8'))

        else:
            print("MESSAGE HANDLER: " + msg['channel'].decode('utf-8'))

        message_content = json.loads(msg['data'])
        print(message_content)


# Connect to the Redis message broker
r = redis.Redis(host='localhost', port=6379, db=0)

# Create the pub sub client
p = r.pubsub()

print("Subscribing to different channels...")

# Subscribe to individual channels and assign the handler
p.subscribe(**{'sensors/garden' : handle_msg})
p.subscribe(**{'sensors/kitchen' : handle_msg})

# Subscribe to various channels using a wildcard
p.psubscribe(**{'sensors/*' : handle_msg})


# This loop is necessary for the callbacks to be triggered.
# If necessary we could implement it in a separated thread
for message in p.listen():
    pass

