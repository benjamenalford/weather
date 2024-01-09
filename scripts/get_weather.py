import pandas as pd
import requests
import time
import json
from datetime import datetime, timedelta

#config
ephemera_url = "http://ira.local:5000/api/weather/add" # local hosted api
url = 'https://data.rcc-acis.org/StnData'  #national weather service API

#get today's date , setting start and end date the same
start_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d') #'2024-1-2'
end_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d') #'2024-1-2'

#prep request parameters
params = '{"elems":[{"name":"maxt","interval":[1,0,0],"duration":1,"smry":[{"reduce":"max"},{"reduce":"mean"},{"reduce":"min"},{"reduce":"pct_ge_100"},{"reduce":"pct_ge_90"},{"reduce":"pct_ge_50"},{"reduce":"pct_le_32"}]},{"name":"mint","interval":[1,0,0],"duration":1,"smry":[{"reduce":"max"},{"reduce":"mean"},{"reduce":"min"},{"reduce":"pct_ge_70"},{"reduce":"pct_ge_50"},{"reduce":"pct_le_32"},{"reduce":"pct_le_0"}]},{"name":"pcpn","interval":[1,0,0],"duration":1,"smry":[{"reduce":"max"},{"reduce":"mean"},{"reduce":"min"},{"reduce":"pct_ge_0.01"},{"reduce":"pct_ge_0.10"},{"reduce":"pct_ge_0.50"},{"reduce":"pct_ge_1.0"}]},{"name":"snow","interval":[1,0,0],"duration":1,"smry":[{"reduce":"max"},{"reduce":"mean"},{"reduce":"min"},{"reduce":"pct_ge_0.1"},{"reduce":"pct_ge_1.0"},{"reduce":"pct_ge_3.0"},{"reduce":"pct_ge_6.0"}]},{"name":"snwd","interval":[1,0,0],"duration":1,"smry":[{"reduce":"max"},{"reduce":"mean"},{"reduce":"min"},{"reduce":"pct_ge_1"},{"reduce":"pct_ge_3"},{"reduce":"pct_ge_6"},{"reduce":"pct_ge_12"}]}],"sid":"TOPthr 9","sDate":"{start_date}","eDate":"{end_date}"}'
params = params.replace('{start_date}', start_date)
params = params.replace('{end_date}', end_date)
param_obj = json.loads(params)

req = requests.post(url, data={'params': params, 'output': 'json'})

#unwrap the request
date, max_temp, min_temp, precip, snow, snow_depth = req.json()['data'][0]
day_data = {'date': date, 'actual_max_temp': max_temp, "actual_min_temp": min_temp,
            "actual_precip": precip, "actual_snow": snow, "actual_snow_depth": snow_depth}

if "T" in day_data.values() or "M" in day_data.values():
    print("missing value T or M found", day_data.values())

#goes to the log
print(day_data)

#send to the DB
requests.post(ephemera_url, json=day_data).text