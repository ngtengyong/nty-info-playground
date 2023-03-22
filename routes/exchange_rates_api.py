from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
from google.cloud import datastore
import datetime
from routes.access_validator import validate_access

exchange_rates_api_bp = Blueprint('exchange_rates_api', __name__)

@exchange_rates_api_bp.route('/exchange-rates', methods=['POST'])
def fetch_exchange_rates():
    # check if apiKey is provided in the request headers
    apiKey = request.headers.get('x-api-key')
    if not apiKey:
        return "Missing of X-API-Key", 401

    # Validate access
    if not validate_access(apiKey):
        return "Access Forbidden", 403

    # Define a list of currency codes to fetch the exchange rates for
    currencies = ['MYR', 'VND', 'PHP', 'THB', 'SGD', 'KHR', 'MMK', 'BND', 'LAK', 'IDR']
    currencies_to_countries = {'MYR': 'Malaysia', 'VND': 'Vietnam', 'PHP': 'Philippines', 'THB': 'Thailand', 'SGD': 'Singapore', 'KHR': 'Cambodia', 'MMK': 'Myanmar', 'BND': 'Brunei', 'LAK': 'Laos', 'IDR': 'Indonesia'}
    exchange_rates = {}

    # Create a client to interact with the Datastore API
    client = datastore.Client()

    # Iterate over each currency and fetch the last rates of yesterday
    previous_rates = {}
    today = datetime.datetime.now()
    yesterday = datetime.datetime(today.year, today.month, today.day, 0, 0, 0) - datetime.timedelta(days=1)
    yesterday_end = datetime.datetime.combine(yesterday, datetime.time.max)
    print (f'date time of yesterday end : {yesterday_end}')
    for currency in currencies:
        query = client.query(kind='exchange_rates')
        query.add_filter('timestamp', '<', yesterday_end)
        query.add_filter('to_currency_code', '=', currency)
        query.order = ['-timestamp']
        previous_rates_entity = list(query.fetch(limit=1))
        if previous_rates_entity:
            print (f'previous_rates_entity = {previous_rates_entity}')
            previous_rate = previous_rates_entity[0]['to']
            previous_rates[currency] = previous_rate 

    print(f'Yesterday rates: {previous_rates}')

    # Iterate over each currency and fetch the exchange rate
    for currency in currencies:
        url = f"https://www.google.com/search?q=1+USD+to+{currency}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.get(url, headers=headers)

        # Parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the exchange rate element and extract the value attribute
        exchange_rate = soup.find('span', {'class': 'DFlfde', 'data-precision': '2', 'data-value': True})['data-value']
        

        # Calculate the percentage change from the previous day
        previous_rate = previous_rates.get(currency, None)
        if previous_rate is not None:
            percentage_change = -1 *((float(exchange_rate) - previous_rate) / previous_rate * 100)
        else:
            percentage_change = None

        # Add the exchange rate to the dictionary
        exchange_rates[currency] = exchange_rate

        # Create an entity and set its properties
        entity = datastore.Entity(key=client.key('exchange_rates'))
        entity.update({
            #'timestamp': (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': datetime.datetime.utcnow(),
            'date': (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d'),
            'from_currency_code': 'USD',
            'from': 1,
            'to_currency_code': currency,
            'to_currency_country': currencies_to_countries[currency],  # Add the to_currency_country property
            'to': float(exchange_rate),
            'percentage_change': percentage_change  # Add the percentage_change property
        })
        print(f"Today's rate = {exchange_rate}. Percentage change = {percentage_change}")

        # Insert the entity into the Datastore
        client.put(entity)

    return "Exchange rates updated successfully"

@exchange_rates_api_bp.route('/country-currency', methods=['POST'])
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

    # Initialize a Google Datastore client
    client = datastore.Client()

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

        # Define a new Datastore entity
        entity = datastore.Entity(key=client.key(kind))
        entity.update({
            "currency_code": currency_code,
            "country_name": country_name,
            "country_code": country_code
        })

        # Insert the entity into Datastore
        client.put(entity)
    return "insert country currency successfully"

@exchange_rates_api_bp.route('/country-to-watch', methods=['POST'])
def write_countries_to_datastore():
    # Create a Datastore client
    client = datastore.Client()

    # Open the CSV file and read the data
    with open('countries.csv', 'r') as file:
        data = file.readlines()

    # Remove the header row
    data = data[1:]

    # Loop through the data and create entities for each country
    entities = []
    for line in data:
        country_name, country_code = line.strip().split(',')
        entity = datastore.Entity(key=client.key('country_to_watch'))
        entity.update({
            'country_name': country_name,
            'country_code': country_code,
        })
        entities.append(entity)

    # Write the entities to Datastore
    client.put_multi(entities)

    print(f"{len(entities)} entities written to Datastore.")
    return "insert country currency successfully"