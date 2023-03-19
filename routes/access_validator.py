from google.cloud import datastore

def validate_access(apiKey, apiSecret):
    # check if apiKey and apiSecret are provided
    if apiKey is None or apiSecret is None:
        # Missing apiKey or apiSecret, return 400 status
        return False
    
    # Create a client to interact with the Datastore API
    client = datastore.Client()
    
    # validate against records in api_access kind
    queryApi = client.query(kind='api_access')
    queryApi.add_filter('key', '=', apiKey)
    queryApi.add_filter('secret', '=', apiSecret)
    api_entity = queryApi.fetch()

    api_entity_list = list(api_entity)
    if not api_entity_list:
        # Unauthorized access
        return False
    
    return True
