#!/bin/bash
#!/bin/env bash
source /home/openhabian/workspace/smartmeter2influxdb/venv/bin/activate
cd /home/openhabian/workspace/smartmeter2influxdb
while [ true ]; do
  python smartmeter2influxdb.py --host 192.168.178.10 --username openhab --password "AnotherSuperbPassword456-" --db "openhab_db" 
  sleep 30
done


