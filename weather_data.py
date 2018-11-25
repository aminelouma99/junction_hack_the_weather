#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import datetime
import time
import json
import ssl
import sys


MQTTHOST   = "ws-hackjunction2018.vaisala-testbed.net"
MQTTPORT   = 8883
MQTTTOPIC  = "luxgw-05195668/+/+"
data_w=[]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}.".format(rc))
    client.subscribe(MQTTTOPIC)

def on_message(client, userdata, msg):
    try:
        with open('data.json', 'w') as outfile:
            print("debug", msg.payload.decode('utf-8'))
            data_w.append(msg.payload.decode('utf-8'))
            json.dump(data_w, outfile)
            
    except:
        print("on_message: json.loads failed....")

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

connOK = False

while(connOK == False):
    print("Connecting to mqtt server")
    try:
        client.connect(host=MQTTHOST, port=MQTTPORT, keepalive=60)
        connOK = True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        connOK = False
    time.sleep(2)

print("Connected")
# Blocking loop to the Mosquitto brokerclient.loop_forever()
client.loop_forever()

