#!/bin/bash
IP=$(hostname  -I | cut -f1 -d' ') KAFKA=$(curl   $(cat /usr/bin/kafka_location.txt)) telegraf -config /usr/bin/telegraf.conf
