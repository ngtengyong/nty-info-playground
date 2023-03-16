from flask import Blueprint, render_template
from google.cloud import datastore
from geopy.geocoders import Nominatim

exchange_rates_bp = Blueprint('exchange_rates', __name__)

def get_latlng(country):
    geolocator = Nominatim(user_agent='my_app')
    location = geolocator.geocode(country)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None
    
@exchange_rates_bp.route('/exchange-rates', methods=['GET'])
def display_exchange_rates():
    # Define a dictionary mapping currency codes to country names
    currencies_to_countries = {
        'MYR': 'Malaysia', 'VND': 'Vietnam', 'PHP': 'Philippines', 'THB': 'Thailand', 
        'SGD': 'Singapore', 'KHR': 'Cambodia', 'MMK': 'Myanmar', 'BND': 'Brunei', 
        'LAK': 'Laos', 'IDR': 'Indonesia'
    }

    # Create a client to interact with the Datastore API
    client = datastore.Client()

    # Initialize a list to store the countries
    countries = []

    # Query for the latest exchange rate record for each currency and map it to its country
    for currency_code, country_name in currencies_to_countries.items():
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
            exchange_rate_record['latlng'] = get_latlng(exchange_rate_record['name'])

            # Append the exchange rate record to the list of countries
            countries.append(exchange_rate_record)

    # Sort the list of countries by currency code
    countries = sorted(countries, key=lambda x: x['currency'])
    # Set the initial center and zoom level of the map
    map_center = [10, 105]  # Geographical coordinates of Southeast Asia
    zoom_level = 5

    # Render the exchange rates template with the list of countries
    return render_template('exchange_rates.html', countries=countries, map_center=map_center, zoom_level=zoom_level)
