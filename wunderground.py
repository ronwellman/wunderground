#!/usr/bin/env python3

import requests
import config

city = 'Augusta'
state = 'GA'
feature = 'conditions'

url = 'http://api.wunderground.com/api/{}/{}/q/{}/{}.json'.format(config.api_key,feature,state,city)

r = requests.get(url)

if r.status_code == 200:
    curr_obs = r.json()['current_observation']
    city = curr_obs['observation_location']['city'].split(',')[-1].strip()
    state = curr_obs['observation_location']['state']
    feelslike_f = curr_obs['feelslike_f']
    temp_f = curr_obs['temp_f']
    observation_time_rfc822 = curr_obs['observation_time_rfc822'][:-6]
    weather = curr_obs['weather']
    wind_mph = curr_obs['wind_mph']
    wind_dir = curr_obs['wind_dir']
    
    output = ['{:<13}{}, {}'.format('Location:',city,state)]
    output.append('{:<13}{}'.format('Time:',observation_time_rfc822))
    output.append('{:<13}{}'.format('Conditions:',weather))
    output.append('{:<13}{} F'.format('Temp:',temp_f))
    output.append('{:<13}{} @ {} MPH'.format('Winds:',wind_dir,wind_mph))

    width = max((len(l) for l in output)) + 4
    print('*' * width)
    for line in output:
        spaces = width - (len(line) + 3) 
        print('| {}'.format(line) + ' ' * spaces + '|')
    print('*' * width)
else:
    print('Failed to retrieve current weather')


