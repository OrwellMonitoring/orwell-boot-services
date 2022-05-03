#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors: Alexandre Serras (alexandreserras@ua.pt), Gonçalo Leal (goncalolealsilva@ua.pt)
# Date: 02-05-2022

# Description:
# Prometheus node exporter metrics fetch and send to kafka

from nis import cat
import os
import json
import time
import socket
import subprocess
import requests
from kafka import KafkaProducer

# getting the IP address
bash_command = ["hostname",  "-I"]
process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
ip_address = process.communicate()[0].decode("utf-8").split(" ")[0]

while True:
    try:
        f=open(os.path.basename('kafka_location.txt'),"r")
        kafka_url = f.read()
        response= requests.get(url=kafka_url).text
        kafka_location=response
        print(kafka_location)

        metrics = requests.get(url="http://localhost:9100/metrics").text
        ts= int(time.time())
        metrics= metrics.split("\n")

        lst=[]
        for metric in metrics :
            if metric.startswith("#") or metric == "":continue
            
            metric = metric.split(" ")
            value=metric[-1]
            properties=metric[:-1]
            
            if len(properties) > 1:
                    properties = "_".join(properties)
            else:
                properties=properties[0]
            
            array = properties.split("{")
            if len(array) > 1:
                properties = { v[0]:v[1].strip("\"}") for v in [ v.split("=") for v in array[1].split(",") ] } if len(array[1]) > 1 else {}
            else:
                properties=dict()

            properties["instance"]= ip_address
            title=array[0]
        
            properties = str(properties).replace(':', '=').replace(' ', '').replace('\'', '"').replace('"=', '=').replace(',"', ',').replace('{"', '{') 
            metric=title+properties+" "+value+" "+str(ts)
            lst.append(metric)

        print(lst)
        
        producer = KafkaProducer(
            bootstrap_servers=[kafka_location],
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        producer.send('prometheus', value=lst)
    except:
        print("Error, maybe")

    time.sleep(15)