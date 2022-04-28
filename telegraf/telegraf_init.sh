#!/bin/bash
IP=$(hostname  -I | cut -f1 -d' ') KAFKA=$(curl  -s $(cat /usr/bin/kafka_location.txt) | python3 -c "import sys, json; print(json.load(sys.stdin)['host'])") telegraf -config /usr/bin/telegraf.conf
