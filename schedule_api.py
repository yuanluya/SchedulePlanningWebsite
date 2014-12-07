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

def get_schools(termCode):
    '''
    Returns a list of valid schools.
    Each item in the list is a dictionary containing:
        ('SchoolCode', 'SchoolDescr', 'SchoolShortDescr') 
    '''
    return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools')['getSOCSchoolsResponse']['School']


def get_subjects(termCode, schoolCode):
    '''
    Return a list of valid subjects(criteria)
    Each item in the list is a dictionary containing:
    ['SubjectCode', 'SubjectDescr', 'SubjectShorDescr']
    '''
    if type(get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+schoolCode+'/Subjects')['getSOCSubjectsResponse']['Subject']) == type([]):
        return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+schoolCode+'/Subjects')['getSOCSubjectsResponse']['Subject']
    else:
        help = []
        help.append(get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+schoolCode+'/Subjects')['getSOCSubjectsResponse']['Subject'])
        return help

def get_classNumbers(termCode, SubjectCode):
    '''
    Return a list of valid class
    Each item in the list is a dictionary
    '''
    return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Classes/Search/'+SubjectCode)['searchSOCClassesResponse']['SearchResult']

def get_classDetailsByClassnumbers(termCode, classNumber):
    '''
    Return details of valid class
    '''
    return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Classes/'+classNumber)['getSOCSectionListByNbrResponse']['ClassOffered']

def get_catalogNumbers(termCode, schoolCode, subjectCode):
    '''
    Return a list of valid catalogNumbers
    Each item in the list is a dictionary
    '''
    return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+schoolCode+'/Subjects/'+subjectCode+'/CatalogNbrs')['getSOCCtlgNbrsResponse']['ClassOffered']

def get_classSections(termCode, SchoolCode, SubjectCode, catalogNumber):
    '''
    Return a list of valid sections and their details of particular section.
    Each item in the list is a dictionary
    '''
    return get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+SchoolCode+'/Subjects/'+SubjectCode+'/CatalogNbrs/'+catalogNumber+'/Sections')['getSOCSectionsResponse']['Section']

def get_className(termCode, SchoolCode, SubjectCode, catalogNumber):
    '''
    Return the name of the course
    '''
    descr = get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+SchoolCode+'/Subjects/'+SubjectCode+'/CatalogNbrs/'+catalogNumber)['getSOCCourseDescrResponse']['CourseDescr']
    try:
        name = descr[0:descr.index('-')-1]
    except ValueError:
        name = descr
        if name.find('\n') != -1: 
            name = name[0:name.find('\n')-1]
    return name

def get_classDescr(termCode, SchoolCode, SubjectCode, catalogNumber):
    '''
    Return the name of the course
    '''
    descr = get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+SchoolCode+'/Subjects/'+SubjectCode+'/CatalogNbrs/'+catalogNumber)['getSOCCourseDescrResponse']['CourseDescr']
    Descr = descr[descr.index('-')+4:]
    return Descr

def get_basicClassInfo(termCode, SchoolCode, SubjectCode, catalogNumber):
    '''
    Return a list of basic information of a course
    '''
    try:
        list1 = get_data('/Curriculum/SOC/v1/Terms/'+termCode+'/Schools/'+SchoolCode+'/Subjects/'+SubjectCode+'/CatalogNbrs/'+catalogNumber+'/Sections')['getSOCSectionsResponse']['Section']
        listX = list1[0]
    except KeyError:
        listX = list1
    name = get_className(termCode, SchoolCode, SubjectCode, catalogNumber)
    pack = {}
    pack['SectionName'] = name
    pack['CreditHours'] = listX['CreditHours']
    pack['CatalogNumber'] = catalogNumber
    pack['SectionType'] = listX['SectionType']

    return pack