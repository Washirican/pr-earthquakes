import requests
import json


def get_earthquakes(url):
    errors = []

    try:
        response = requests.get(url)
        recent_eq_data = response.json()
        return recent_eq_data
    except:
        errors.append('Unable to get URL.')
        return {'error': errors}
