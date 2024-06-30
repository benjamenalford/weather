import requests
import json
from datetime import datetime, timedelta
import logging

# config
CONFIG = {
    'ephemera_url': "http://ira.local:5000/api/weather/add",  # local hosted api
    'nws_url': 'https://data.rcc-acis.org/StnData'  # national weather service API
}

def fetch_weather(start_date, end_date):
    try:
        ob = {
    'elems': [
        {
            'name': 'maxt',
            'interval': [1, 0, 0],
            'duration': 1,
            'smry': [
                {'reduce': 'max'},
                {'reduce': 'mean'},
                {'reduce': 'min'},
                {'reduce': 'pct_ge_100'},
                {'reduce': 'pct_ge_90'},
                {'reduce': 'pct_ge_50'},
                {'reduce': 'pct_le_32'}
            ]
        }, {
            'name': 'mint',
            'interval': [1, 0, 0],
            'duration': 1,
            'smry': [
                {'reduce': 'max'},
                {'reduce': 'mean'},
                {'reduce': 'min'},
                {'reduce': 'pct_ge_70'},
                {'reduce': 'pct_ge_50'},
                {'reduce': 'pct_le_32'},
                {'reduce': 'pct_le_0'}
            ]
        }, {
            'name': 'pcpn',
            'interval': [1, 0, 0],
            'duration': 1,
            'smry': [
                {'reduce': 'max'},
                {'reduce': 'mean'},
                {'reduce': 'min'},
                {'reduce': 'pct_ge_0.01'},
                {'reduce': 'pct_ge_0.10'},
                {'reduce': 'pct_ge_0.50'},
                {'reduce': 'pct_ge_1.0'}]
        },
        {
            'name': 'snow',
            'interval': [1, 0, 0],
            'duration': 1,
            'smry': [
                {'reduce': 'max'},
                {'reduce': 'mean'},
                {'reduce': 'min'},
                {'reduce': 'pct_ge_0.1'},
                {'reduce': 'pct_ge_1.0'},
                {'reduce': 'pct_ge_3.0'},
                {'reduce': 'pct_ge_6.0'}]
        },
        {
            'name': 'snwd',
            'interval': [1, 0, 0],
            'duration': 1,
            'smry': [
                {'reduce': 'max'},
                {'reduce': 'mean'},
                {'reduce': 'min'},
                {'reduce': 'pct_ge_1'},
                {'reduce': 'pct_ge_3'},
                {'reduce': 'pct_ge_6'},
                {'reduce': 'pct_ge_12'}
            ]
        }
    ],
    'sid': 'TOPthr 9',
    'sDate': start_date,
    'eDate': end_date}

        req = requests.post(CONFIG['nws_url'], data={'params': json.dumps(ob), 'output': 'json'})

        if req.status_code != 200:
            logging.error("Failed to get weather data from NWS API")
            return None

        date, max_temp, min_temp, precip, snow, snow_depth = req.json()['data'][0]
        day_data = {
            'date': date,
            'actual_max_temp': max_temp,
            "actual_min_temp": min_temp,
            "actual_precip": precip,
            "actual_snow": snow,
            "actual_snow_depth": snow_depth,
            "date_added": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        if "T" not in day_data or "M" not in day_data:
            logging.error("Missing required values T or M in the weather data")
            return None

        req = requests.post(CONFIG['ephemera_url'], json=day_data)

        if req.status_code != 200:
            logging.error("Failed to write to database")
            return None

        logging.info(f"Successfully added weather data for {date}")
        return day_data

    except Exception as e:
        logging.exception(str(e))
        return None

if __name__ == "__main__":
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()
    weather_data = fetch_weather(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))