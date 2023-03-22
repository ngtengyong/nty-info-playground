from flask import Blueprint, request
import requests
from google.cloud import datastore
import datetime
from routes.access_validator import validate_access

setup_api_bp = Blueprint('setup_api', __name__)

client = datastore.Client()

@setup_api_bp.route('/populate-country-currency', methods=['POST'])
def insert_country_currecy():
    # check if apiKey is provided in the request headers
    apiKey = request.headers.get('x-api-key')
    if not apiKey:
        return "Missing of X-API-Key", 401

    # Validate access
    if not validate_access(apiKey):
        return "Access Forbidden", 403

    # Define the REST Countries API endpoint
    url = "https://restcountries.com/v3.1/all"

    # Make a GET request to the API and retrieve the JSON data
    response = requests.get(url)
    data = response.json()

    # Define the Datastore Kind
    kind = "country_currency"

    # Loop through the data and insert each currency code and country name into Datastore
    for country in data:
        if "currencies" in country:
            currency_code = list(country["currencies"].keys())[0]
        else:
            currency_code = "Unknown"

        country_name = country["name"]["common"]
        
        # Get the country code, if it exists
        if "cca2" in country:
            country_code = country["cca2"]
        else:
            country_code = "Unknown"

        print (f'country = {country_name} ({country_code}) currency code = {currency_code} ')            

        # Query Datastore to check if the country already exists
        query = client.query(kind=kind)
        query.add_filter("country_name", "=", country_name)
        result = list(query.fetch())

        # If the country already exists, skip inserting the new entity
        if result:
            continue            

        # Define a new Datastore entity
        entity = datastore.Entity(key=client.key(kind))
        entity.update({
            "currency_code": currency_code,
            "country_name": country_name,
            "country_code": country_code,
            'timestamp': datetime.datetime.utcnow(),
        })
        
        print (f'INSERT entity FOR country = {country_name} ({country_code}) currency code = {currency_code} ')

        # Insert the entity into Datastore
        client.put(entity)
    return "insert country currency successfully"

@setup_api_bp.route('/import-country-to-watch', methods=['POST'])
def insert_country_to_watch():
    kind = 'country_to_watch'

    # Open the CSV file and read the data
    with open('countries.csv', 'r') as file:
        data = file.readlines()

    # Remove the header row
    data = data[1:]

    # Loop through the data and create entities for each country
    entities = []
    for line in data:
        country_name, country_code = line.strip().split(',')
        # Query Datastore to check if the country already exists
        query = client.query(kind=kind)
        query.add_filter("country_code", "=", country_code)
        result = list(query.fetch())

        # If the country already exists, skip inserting the new entity
        if result:
            continue     

        entity = datastore.Entity(key=client.key(kind))
        entity.update({
            'country_name': country_name,
            'country_code': country_code,
            'timestamp': datetime.datetime.utcnow(),
        })
        entities.append(entity)

    # Write the entities to Datastore
    client.put_multi(entities)

    print(f"{len(entities)} entities written to Datastore.")
    return "insert country currency successfully"