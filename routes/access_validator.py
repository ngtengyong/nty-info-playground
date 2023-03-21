from google.cloud import datastore

def validate_access(apiKey):
    # check if apiKey and apiSecret are provided
    if apiKey is None:
        # Missing apiKey, return 400 status
        return False
    
    # Create a client to interact with the Datastore API
    client = datastore.Client()
    
    # validate against records in api_access kind
    queryApi = client.query(kind='api_access')
    queryApi.add_filter('key', '=', apiKey)
    api_entity = queryApi.fetch()

    api_entity_list = list(api_entity)
    if not api_entity_list:
        # Unauthorized access
        return False
    
    return True
