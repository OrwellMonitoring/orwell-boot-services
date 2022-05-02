#!/bin/bash
/usr/local/bin/node_exporter &
sleep 5
cd /usr/local/etc/node/ && python3 main.py