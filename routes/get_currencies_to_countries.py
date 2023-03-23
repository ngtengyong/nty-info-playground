from google.cloud import datastore

def get_currencies():
    client = datastore.Client()
    # get country codes
    query1 = client.query(kind='country_to_watch')
    entities1 = list(query1.fetch())
    country_codes = [entity1['country_code'] for entity1 in entities1]
    # get currency code of country codes above
    query2 = client.query(kind='country_currency')
    entities2 = list(query2.fetch())
    currencies_to_countries = {}
    for entity2 in entities2:
        #print (f'entity = {entity2["country_code"]}')
        if entity2['country_code'] in country_codes:
            currencies_to_countries[entity2['currency_code']] = entity2['country_name']
    # Print the results
    print('Currencies to W A T C H !:', currencies_to_countries.keys())
    return currencies_to_countries