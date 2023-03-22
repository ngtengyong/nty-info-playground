from google.cloud import datastore

def get_currencies():
    client = datastore.Client()
    # get country codes
    query = client.query(kind='country_to_watch')
    entities = list(query.fetch())
    country_codes = [entity['country_code'] for entity in entities]
    # get currency code of country codes above
    query = client.query(kind='country_currency')
    entities = list(query.fetch())
    currencies_to_countries = {}
    for entity in entities:
        if entity['country_code'] in country_codes:
            currencies_to_countries[entity['currency_code']] = entity['country_name']
    # Print the results
    print('Currencies to W A T C H !:', currencies_to_countries.keys())
    return currencies_to_countries