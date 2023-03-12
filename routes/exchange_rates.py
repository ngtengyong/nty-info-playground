from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
from google.cloud import datastore
import datetime

exchange_rates_bp = Blueprint('exchange_rates', __name__)

@exchange_rates_bp.route('/exchange-rates', methods=['POST'])
def fetch_exchange_rates():
    # Define the currencies to search for
    currencies = ['MYR','VND','PHP','THB','SGD','KHR','MMK','BND','LAK','IDR']
    exchange_rates = {}

    # Create a client to interact with the Datastore API
    client = datastore.Client()

    # Iterate over each currency and fetch the exchange rate
    for currency in currencies:
        url = f"https://www.google.com/search?q=1+USD+to+{currency}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.get(url, headers=headers)

        # Parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the exchange rate element and extract the value attribute
        exchange_rate = soup.find('span', {'class': 'DFlfde', 'data-precision': '2', 'data-value': True})['data-value']

        # Add the exchange rate to the dictionary
        exchange_rates[currency] = exchange_rate

        # Create an entity and set its properties

        entity = datastore.Entity(key=client.key('exchange_rates'))
        entity.update({
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'from_currency_code': 'USD',
            'from': 1,
            'to_currency_code': currency,
            'to': float(exchange_rate)
        })

        # Insert the entity into the Datastore
        
        client.put(entity)

    return "Exchange rates updated successfully"
