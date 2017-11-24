# -*- coding: utf-8 -*-

import argparse

import math
import datetime
import time
import requests
from jsonpath import jsonpath
#from jsonpath import JsonPath

from influxdb import InfluxDBClient

def main(username, password, db, host='localhost', port='8086', smartmeter_url='http://127.0.0.1:8081/last/1'):
    now = datetime.datetime.now()
 
    r = requests.get(smartmeter_url)
    json = r.json()

    power_l1 = float(jsonpath(json, "$.Power.L1")[0]);
    #print(power_l1)
    power_l2 = float(jsonpath(json, "$.Power.L2")[0]);
    #print(power_l2)
    power_l3 = float(jsonpath(json, "$.Power.L3")[0]);
    #print(power_l2)

    import_l1 = float(jsonpath(json, "$.Import.L1")[0]);
    #print(power_l1)
    import_l2 = float(jsonpath(json, "$.Import.L2")[0]);
    #print(power_l2)
    import_l3 = float(jsonpath(json, "$.Import.L3")[0]);
    #print(power_l2)
    import_total = float(jsonpath(json, "$.TotalImport")[0]);



    point_power = [{
            "measurement": "smartmeter_power",
            "time": str(datetime.datetime.now()),
            "fields": {
                "L1": power_l1,
                "L2": power_l2,
                "L3": power_l3,
                "Total": float(power_l1 + power_l2 + power_l3)
            }
        }]
    
    point_import = [{
            "measurement": "smartmeter_import",
            "time": str(datetime.datetime.now()),
            "fields": {
                "L1": import_l1,
                "L2": import_l2,
                "L3": import_l3,
                "Total": float(import_total)
            }
        }]
 
    client = InfluxDBClient(host, port, username, password, db)
    client.switch_database(db)
    client.write_points(point_power)
    client.write_points(point_import)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Query smartmeter and write to influxdb')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    parser.add_argument('--username', type=str, required=True,
                        help='username for login')
    parser.add_argument('--password', type=str, required=True,
                        help='password for login')
    parser.add_argument('--db', type=str, required=True,
                        help='database to use')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port, username=args.username, password=args.username, db=args.db)

