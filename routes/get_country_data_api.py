from flask import Blueprint, request
import requests
import json
from google.cloud import datastore
import datetime
import requests
from routes.access_validator import validate_access

get_country_data_api_bp = Blueprint('get_country_data_api', __name__)

import requests

def get_population_data():
    year = 2021
    url = "https://api.worldbank.org/v2/country/"
    countries = ['MY', 'VN', 'PH', 'TH', 'SG', 'KH', 'MM', 'BN', 'LA', 'ID']
    population_data = []
    for country_code in countries:
        query = f"{country_code}/indicator/SP.POP.TOTL?format=json&per_page=1&date={2021}"
        response = requests.get(url + query)
        data = response.json()
        population = data[1][0]['value']
        country_code = country_code
        country_name = data[1][0]['country']['value'].replace('&', 'and')
        population_data.append({'country_code': country_code, 'country': country_name, 'population': population, 'year' : 2021})
        print(f"year: {year} - country: {country_name} ({country_code}) population = {population}")

    return population_data

@get_country_data_api_bp.route('/country-data', methods=['POST'])
def write_to_datastore():
    # check if apiKey and apiSecret are provided in the request
    apiKey = request.json.get('key')
    apiSecret = request.json.get('secret')

    # Validate access
    if not validate_access(apiKey, apiSecret):
        return "Access Forbidden", 403

    client = datastore.Client()
    population_data = get_population_data()
    for country in population_data:
        key = client.key('population')
        entity = datastore.Entity(key=key)
        entity.update({
            'year' : country['year'],
            'country_code' : country['country_code'],
            'country_name': country['country'],
            'population': country['population'],
            'timestamp': datetime.datetime.utcnow()
        })
        client.put(entity)

    return "Insert population data successfully"



