import httplib
import base64
import json
import time
from app import schedule_api_consumer_key as consumer_key
from app import schedule_api_secret_key as secret_key

class ScheduleApiError(Exception):
    '''
    Raised if there is an error with the schedule API.
    '''
    def __init__(self, message=None):
        self.message = message

# The base API endpoint
base_url = 'api-gw.it.umich.edu'

def get_auth_token():
    '''
    Gets an auth token using method described in:
        http://developer.it.umich.edu/api/help#tokens

    Returns a tuple of (access_token, token_expiration)
    '''
    combined = base64.b64encode(consumer_key + ':' + secret_key)
    conn = httplib.HTTPSConnection('api-km.it.umich.edu')
    token_head = {
        'Authorization' : 'Basic ' + combined,
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    conn.request('POST', '/token', \
        'grant_type=client_credentials&scope=PRODUCTION', token_head)
    r = conn.getresponse()
    if r.status != 200:
        raise ScheduleApiError('error when getting auth token')
    data = json.loads(r.read())
    return data['access_token'], float(data['expires_in'])

def get_headers():
    '''
    Gets the necessary headers to make an API request,
    renewing the auth token if needed.
    '''
    if time.time() >= get_headers.expiration - 20:
        get_headers.auth_token, get_headers.expiration = get_auth_token()
        get_headers.expiration += time.time()
    return { 'Authorization' : 'Bearer ' + get_headers.auth_token }
get_headers.expiration = -1.
get_headers.auth_token = ''

def get_data(relative_path):
    '''
    Gets data from the schedule API at the specified path.
    Will raise a ScheduleApiError if unsuccessful.
    Assumes API will return JSON, returns as a dictionary.
    '''
    conn = httplib.HTTPConnection(base_url)
    conn.request(method='GET', url=relative_path, headers=get_headers())
    r = conn.getresponse()

    if r.status != 200:
        raise ScheduleApiError(r.read())
    return json.loads(r.read())

def get_terms():
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('TermCode', 'TermDescr', 'TermShortDescr') 
    '''
    return get_data('/Curriculum/SOC/v1/Terms')['getSOCTermsResponse']['Term']
