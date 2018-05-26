#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegraf is auxliary script who connect into MQTT brouker and read message from this brouker and send this information into influxDB
# main use is for visulisatin mqtt sensor data from domoticz home automation system to visualisation program GRAFANA
# project influxDB contain telegraf program for sending variou types data, but domotic most information send into mqtt as string 
# and oreginal telegraf not have jet conversint into number. Number is necessary for corect visualise data
# PS: 	influxDB is for store data from sensors
#		GRAFANA visualize data from influxDB
# domoticz ----> MQTT bouker -----> telegraf ------> influxDB -----> GRAFANA ----> client web page

#import mosquitto
import paho.mqtt.client as paho
#import urllib2
#import urllib
#import contextlib
#import socket
import json
import time
import os
import pprint
from influxdb import InfluxDBClient

x=1
f=1

def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	parsed_json = json.loads(str(msg.payload))
	#pprint.pprint(parsed_json)
	idx = int(parsed_json['idx'])
	name =  str(parsed_json['name'])
	stype = parsed_json['stype']
	nvalue = parsed_json['nvalue']
	svalue = parsed_json['svalue1']
	if (stype=="Switch"):
		value=float(nvalue)
		text=""
	elif (stype!="Text"):
		value=float(svalue)
		text=""
	else:
		value=str(svalue)
	print (str(idx)+" : "+ str(value) )
	json_body = [
		{
			"measurement": "domoticz",
			"tags": {
				"IDX": idx,
			},
			"fields": {
				"idx": idx,
				name: value,
			}
		}]
	influxDBclient.write_points(json_body)
		
	
influxDBclient = InfluxDBClient('localhost', 8086 )
#influxDBclient.switch_database('telegraf')
influxDBclient.switch_database('demo')
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('localhost',1883)
client.subscribe("domoticz/out")
client.loop_forever()
client.disconnect()




