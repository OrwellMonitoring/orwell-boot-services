#!/bin/bash
/usr/local/bin/node_exporter &
sleep 5
python3 /usr/local/etc/node/main.py