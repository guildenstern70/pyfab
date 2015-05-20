""" 
 FableMe.com
 A LittleLite Web Application
 
 utils.py
 
"""

import os
import logging
import time
import datetime

CHROME_DATE_FORMAT = '%Y-%m-%d'
IE10_DATE_FORMAT = '%m/%d/%Y'
OUTPUT_PATH = "output/"
RESOURCES_PATH = "resources/"
PRODUCTION_DOMAIN = "fableomatic.appspot.com"


class BasicUtils(object):
    
    @staticmethod
    def get_production_domain():
        return PRODUCTION_DOMAIN
    
    @staticmethod
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

    @staticmethod    
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
    
    @staticmethod
    def string_to_date(inputstring):
        """ Convert a string read from an <input type='date'> to a date """
        if BasicUtils.is_date_valid(inputstring, CHROME_DATE_FORMAT):
            logging.debug('Trying to convert #' + inputstring + '#: it seems a CHROME date...') 
            retdt = BasicUtils.convert_date(inputstring, CHROME_DATE_FORMAT)
        elif BasicUtils.is_date_valid(inputstring, IE10_DATE_FORMAT):
            logging.debug('Trying to convert #' + inputstring + '# it seems a IE10 date...') 
            retdt = BasicUtils.convert_date(inputstring, IE10_DATE_FORMAT)
        else:
            logging.debug('Cannot convert date. Defaulting to 01/01/2000')
            retdt = datetime.date(2000, 01, 01)
        return retdt

    @staticmethod
    def get_output_path(filename):
        return os.path.join(OUTPUT_PATH, filename)
 
    @staticmethod   
    def get_from_relative_resources(filename):
        return os.path.join(RESOURCES_PATH, filename)

    @staticmethod    
    def normalize_path(filename):
        """ Normalize a path under Google App Engine """
        return os.path.normpath(filename) 
    
    
class GoogleUtils(BasicUtils):

    @staticmethod
    def get_from_relative_resources(filename):
        return os.path.join(RESOURCES_PATH, filename)

    @staticmethod
    def get_from_google(filename):
        """ Get the absolute path of a file stored under Google App Engine """
        return GoogleUtils.__get_google_app_path(filename) 
    
    @staticmethod
    def get_from_resources(filename):
        """ Get a file stored in RESOURCE_PATH under Google App Engine """
        filepath = GoogleUtils.get_from_relative_resources(filename)
        return GoogleUtils.__get_google_app_path(filepath)

    @staticmethod
    def __get_google_app_path(filepath):
        dirpath = os.path.dirname(os.path.split(__file__)[0])
        abnormpath = os.path.join(dirpath, filepath) 
        return os.path.normpath(abnormpath)
