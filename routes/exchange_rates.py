from flask import Blueprint, render_template
from google.cloud import datastore

exchange_rates_bp = Blueprint('exchange_rates', __name__)

# @exchange_rates_bp.route('/exchange-rates', methods=['GET'])
# def display_exchange_rates():
#     # Create a client to interact with the Datastore API
#     client = datastore.Client()

#     query = client.query(kind='exchange_rates')
#     query.order = ['-timestamp']
#     query_dict = {}
#     for rate in query.fetch():
#         if rate['to_currency_code'] not in query_dict:
#             query_dict[rate['to_currency_code']] = rate
#     result = query_dict.values()

#     # Execute the query and get all results
#     results = list(query.fetch())

#     # Define a dictionary mapping currency codes to country names
#     currencies_to_countries = {'MYR': 'Malaysia', 'VND': 'Vietnam', 'PHP': 'Philippines', 'THB': 'Thailand', 'SGD': 'Singapore', 'KHR': 'Cambodia', 'MMK': 'Myanmar', 'BND': 'Brunei', 'LAK': 'Laos', 'IDR': 'Indonesia'}

#     # Initialize a list to store the exchange rate records
#     exchange_rates_records = []

#     # Loop over all entities and extract the relevant information
#     for entity in results:
#         exchange_rate_record = {
#             'to_currency_code': entity['to_currency_code'],
#             'equivalent_value': entity['to'],
#             'last_updated_on': entity['timestamp']
#         }

#         # Check if the entity has a 'to_currency_country' property
#         if 'to_currency_country' in entity:
#             exchange_rate_record['country'] = entity['to_currency_country']
#         else:
#             # Use the currencies_to_countries mapping to get the country name
#             exchange_rate_record['country'] = currencies_to_countries.get(entity['to_currency_code'])

#         exchange_rates_records.append(exchange_rate_record)

#     # Render the exchange rates template with the records
#     return render_template('exchange_rates.html', records=exchange_rates_records)

@exchange_rates_bp.route('/exchange-rates', methods=['GET'])
def display_exchange_rates():
    # Create a client to interact with the Datastore API
    client = datastore.Client()

    # Define a dictionary mapping currency codes to country names
    currencies_to_countries = {'MYR': 'Malaysia', 'VND': 'Vietnam', 'PHP': 'Philippines', 'THB': 'Thailand', 'SGD': 'Singapore', 'KHR': 'Cambodia', 'MMK': 'Myanmar', 'BND': 'Brunei', 'LAK': 'Laos', 'IDR': 'Indonesia'}

    # Initialize a dictionary to store the latest exchange rate record for each currency
    latest_exchange_rates = {}

    # Query for the latest exchange rate record for each currency
    for currency_code in currencies_to_countries:
        query = client.query(kind='exchange_rates')
        query.add_filter('to_currency_code', '=', currency_code)
        query.order = ['-timestamp']
        result = list(query.fetch(limit=1))

        if result:
            entity = result[0]
            exchange_rate_record = {
                'to_currency_code': entity['to_currency_code'],
                'equivalent_value': entity['to'],
                'last_updated_on': entity['timestamp']
            }
            # Use the currencies_to_countries mapping to get the country name
            exchange_rate_record['country'] = currencies_to_countries[entity['to_currency_code']]
            latest_exchange_rates[currency_code] = exchange_rate_record

    # Convert the dictionary to a list of records and sort by currency code
    exchange_rates_records = sorted(list(latest_exchange_rates.values()), key=lambda x: x['to_currency_code'])

    # Render the exchange rates template with the records
    return render_template('exchange_rates.html', records=exchange_rates_records)
