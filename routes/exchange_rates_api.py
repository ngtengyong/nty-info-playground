from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
from google.cloud import datastore
import datetime
from routes.access_validator import validate_access
from routes.get_currencies_to_countries import get_currencies

exchange_rates_api_bp = Blueprint('exchange_rates_api', __name__)

client = datastore.Client()
   
def get_previous_rates():
    # Iterate over each currency and fetch the last rates of yesterday
    previous_rates = {}
    today = datetime.datetime.now()
    yesterday = datetime.datetime(today.year, today.month, today.day, 0, 0, 0) - datetime.timedelta(days=1)
    yesterday_end = datetime.datetime.combine(yesterday, datetime.time.max)
    print (f'date time of yesterday end : {yesterday_end}')

    currencies_to_countries = get_currencies()

    for currency in currencies_to_countries.keys():
        query = client.query(kind='exchange_rates')
        query.add_filter('timestamp', '<', yesterday_end)
        query.add_filter('to_currency_code', '=', currency)
        query.order = ['-timestamp']
        previous_rates_entity = list(query.fetch(limit=1))
        if previous_rates_entity:
            #print (f'previous_rates_entity = {previous_rates_entity}')
            previous_rate = previous_rates_entity[0]['to']
            previous_rates[currency] = previous_rate 

    # print(f'Yesterday rates: {previous_rates}')
    return previous_rates

@exchange_rates_api_bp.route('/exchange-rates', methods=['POST'])
def fetch_exchange_rates():
    # check if apiKey is provided in the request headers
    apiKey = request.headers.get('x-api-key')
    if not apiKey:
        return "Missing of X-API-Key", 401

    # Validate access
    if not validate_access(apiKey):
        return "Access Forbidden", 403

    exchange_rates = {}
    #currencies_to_countries = get_currencies()
    currencies = get_currencies()

    previous_rates = get_previous_rates()
    # Iterate over each currency and fetch the exchange rate
    for currency_code, country_name in currencies.items():
        url = f"https://www.google.com/search?q=1+USD+to+{currency_code}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.get(url, headers=headers)

        # Parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the exchange rate element and extract the value attribute
        exchange_rate = soup.find('span', {'class': 'DFlfde', 'data-precision': '2', 'data-value': True})['data-value']
        # Calculate the percentage change from the previous day
        previous_rate = previous_rates.get(currency_code, None)
        if previous_rate is not None:
            percentage_change = -1 *((float(exchange_rate) - previous_rate) / previous_rate * 100)
        else:
            percentage_change = None

        # Add the exchange rate to the dictionary
        exchange_rates[currency_code] = exchange_rate

        # Create an entity and set its properties
        entity = datastore.Entity(key=client.key('exchange_rates'))
        entity.update({
            #'timestamp': (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': datetime.datetime.utcnow(),
            'date': (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d'),
            'from_currency_code': 'USD',
            'from': 1,
            'to_currency_code': currency_code,
            'to_currency_country': country_name,  # Add the to_currency_country property
            'to': float(exchange_rate),
            'percentage_change': percentage_change  # Add the percentage_change property
        })
        print(f"Today's {currency_code} rate = {exchange_rate}. Percentage change = {percentage_change}")

        # Insert the entity into the Datastore
        client.put(entity)

    return "Exchange rates updated successfully"