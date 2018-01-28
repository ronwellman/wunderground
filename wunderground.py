#!/usr/bin/env python3
'''
    wunderground

    This CLI app utilizes the Weather Underground API to query
    basic weather conditions for a given city/state or zip code.

    Dependencies:
        requests, argparse

    Required Command Line Arguments:
        -c City
        -s State
        -z Zipcode

    API key:
        imported from separate config file
'''
import sys
import argparse
import requests
import config

def parse_json(req):
    '''
    parse_json(requests) -> list

    parse_json takes in a requests object and extracts location, time,
    temperature, and winds information and returns a list containing
    that information preformated for display
    '''
    curr_obs = req.json()['current_observation']
    city = curr_obs['observation_location']['city'].split(',')[-1].strip()
    state = curr_obs['observation_location']['state']
    temp_f = curr_obs['temp_f']
    observation_time_rfc822 = curr_obs['observation_time_rfc822'][:-6]
    weather = curr_obs['weather']
    wind_mph = curr_obs['wind_mph']
    wind_dir = curr_obs['wind_dir']

    output = ['{:<13}{}, {}'.format('Location:', city, state)]
    output.append('{:<13}{}'.format('Time:', observation_time_rfc822))
    output.append('{:<13}{}'.format('Conditions:', weather))
    output.append('{:<13}{} F'.format('Temp:', temp_f))
    output.append('{:<13}{} @ {} MPH'.format('Winds:', wind_dir, wind_mph))

    return output




def main():
    '''
    main() -> int

    Utilizes the requests module to query the Weather Underground http
    API and parses through the resulting JSON to extract location
    specific weather information.
    '''
    parser = argparse.ArgumentParser(description='CLI app for looking up the weather'\
            ' given City/State or Zip')
    parser.add_argument('-c', dest='city', help='City to lookup')
    parser.add_argument('-s', dest='state', help='State to lookup')
    parser.add_argument('-z', dest='zipcode', help='Zipcode to lookup')
    args = parser.parse_args()

    city = args.city
    state = args.state
    zipcode = args.zipcode
    feature = 'conditions'

    if zipcode:
        url = 'http://api.wunderground.com/api/{}/{}/q/{}.json'.format(\
                config.api_key, feature, zipcode)
    else:
        url = 'http://api.wunderground.com/api/{}/{}/q/{}/{}.json'.format(\
                config.api_key, feature, state, city)

    req = requests.get(url)

    if req.status_code == 200:
        output = parse_json(req.json())
        width = max((len(l) for l in output)) + 4
        print('*' * width)
        for line in output:
            spaces = width - (len(line) + 3)
            print('| {}'.format(line) + ' ' * spaces + '|')
        print('*' * width)
    else:
        print('Failed to retrieve current weather')

    return 0

if __name__ == "__main__":
    sys.exit(main())
