#!/usr/bin/env python3

import requests
import config

city = 'Augusta'
state = 'GA'
feature = 'conditions'

url = 'http://api.wunderground.com/api/{}/{}/q/{}/{}.json'.format(config.api_key,feature,state,city)

r = requests.get(url)

if r.status_code == 200:
    print('It feels like {}F out there!'.format(r.json()['current_observation']['feelslike_f']))
