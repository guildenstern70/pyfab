""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 pages.py

"""

import os
import logging
import time
import datetime

CHROME_DATE_FORMAT = '%Y-%m-%d'
IE10_DATE_FORMAT = '%m/%d/%Y'
RESOURCES_PATH = '../resources/'

def get_from_resources(filename):
    """ Get a file stored in RESOURCE_PATH under Google App Engine """
    filepath = os.path.join(RESOURCES_PATH, filename)
    return get_google_app_path(filepath) 

def get_google_app_path(filepath):
    """ Return the path of a file
        inside the google appengine framework """
    return os.path.join(os.path.split(__file__)[0], filepath) 

def is_date_valid(inputstring, inputformat):
    """ Check if the input string contains
        a date in the format specified """
    was_converted = False
    try:
        struct_dt = time.strptime(inputstring, inputformat)
        logging.debug('StructDT = ' + str(struct_dt)) 
        datetime.date.fromtimestamp(time.mktime(struct_dt))
        was_converted = True
    except ValueError:
        logging.debug('Unknown date format for '+inputstring+': defaulting...')
    return was_converted

def convert_date(inputstring, inputformat):
    """ Convert string to a date """
    retdt = None
    try:
        struct_dt = time.strptime(inputstring, inputformat)
        retdt = datetime.date.fromtimestamp(time.mktime(struct_dt))
    except ValueError:
        logging.debug('Cannot convert date. Defaulting to 01/01/2000')
        retdt = datetime.date(2000,01,01)
    return retdt

def string_to_date(inputstring):
    """ Convert a string read from an <input type='date'> to a date """
    retdt = None   
    if (is_date_valid(inputstring, CHROME_DATE_FORMAT)):
        logging.debug('Trying to convert #' + inputstring + '#: it seems a CHROME date...') 
        retdt = convert_date(inputstring, CHROME_DATE_FORMAT)
    elif (is_date_valid(inputstring, IE10_DATE_FORMAT)): 
        logging.debug('Trying to convert #' + inputstring + '# it seems a IE10 date...') 
        retdt = convert_date(inputstring, IE10_DATE_FORMAT)
    else:
        logging.debug('Cannot convert date. Defaulting to 01/01/2000')
        retdt = datetime.date(2000,01,01)
    return retdt

