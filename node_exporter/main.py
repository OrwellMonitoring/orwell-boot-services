import json
import time
from datetime import datetime
import requests 


while True:
    f=open("kakfa_location.txt","r")
    kafka_url = f.read()
    response= requests.get(url=kafka_url).text
    kafka_location=response
    metrics = requests.get(url="http://localhost:9100/metrics").text
    ts= int(time.time())
    ## getting the IP address using socket.gethostbyname() method
    ip_address = requests.get('https://api.ipify.org').text
    #ip_address= socket.gethostbyname(socket.gethostname() )
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
        metric=title+str(properties)+" "+value+" "+str(ts)
        #print(metric)
        lst.append(metric)
    print(lst)
    #escrever a metrica no kafka e adicionar lhe a instance
    #mandar metrica a metrica ou a list logo toda? 
    time.sleep(15)