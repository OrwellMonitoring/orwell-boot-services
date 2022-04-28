#!/bin/bash
if [  -f ./ip_host ] then
hostname  -I | cut -f1 -d' ' > ./ip_host;
fi
IP=$(cat ./ip_host) KAFKA=$(curl  -s '10.0.12.82:8008/service_discovery/kafka/' | python3 -c "import sys, json; print(json.load(sys.stdin)['host'])") telegraf -config /usr/bin/telegraf.conf
