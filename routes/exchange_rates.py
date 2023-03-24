from flask import Blueprint, render_template
from google.cloud import datastore
from geopy.geocoders import Nominatim
from routes.get_currencies_to_countries import get_currencies

exchange_rates_bp = Blueprint('exchange_rates', __name__)

def get_latlng(country):
    geolocator = Nominatim(user_agent='my_app')
    location = geolocator.geocode(country)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None
    
# Create a client to interact with the Datastore API
client = datastore.Client()

# Define a function to get the currency code from the country name
def get_currency_code(country_name):
    query = client.query(kind='country_currency')
    query.add_filter('country_name', '=', country_name)
    result = list(query.fetch())
    if result:
        return result[0]['currency_code']
    else:
        return None    
    
@exchange_rates_bp.route('/exchange-rates', methods=['GET'])
def display_exchange_rates():
    # Initialize a list to store the countries
    countries = []
    currencies = get_currencies()

    # Query for the latest exchange rate record for each currency and map it to its country
    for currency_code, country_name in currencies.items():
        query = client.query(kind='exchange_rates')
        query.add_filter('to_currency_code', '=', currency_code)
        query.order = ['-timestamp']
        result = list(query.fetch(limit=1))

        if result:
            entity = result[0]
            exchange_rate_record = {
                'currency': entity['to_currency_code'],
                'value': entity['to'],
                'last_updated_on': entity['timestamp'],
                'name': country_name,
                'perc_change' : entity['percentage_change']
            }

            # Get the latlng of the country
            exchange_rate_record['latlng'] = get_latlng(country_name)
            # Append the exchange rate record to the list of countries
            countries.append(exchange_rate_record)

    # Sort the list of countries by currency code
    countries = sorted(countries, key=lambda x: x['currency'])
    # Set the initial center and zoom level of the map
    map_center = [0, 120]  # Geographical coordinates of Southeast Asia
    zoom_level = 3

    # Render the exchange rates template with the list of countries
    return render_template('exchange_rates.html', countries=countries, map_center=map_center, zoom_level=zoom_level)
