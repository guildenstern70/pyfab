""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 fabulator.py
 
"""

# pylint: disable=C0301

import logging
import time
import datetime

from fableme.version import version
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser
from google.appengine.api import users

CHROME_DATE_FORMAT = '%Y-%m-%d'
IE10_DATE_FORMAT = '%m/%d/%Y'

def is_inputstring_valid(inputstring, inputformat):
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
    retdt = None
    try:
        struct_dt = time.strptime(inputstring, inputformat)
        retdt = datetime.date.fromtimestamp(time.mktime(struct_dt))
    except ValueError:
        logging.debug('Cannot convert date. Defaulting to 01/01/2000')
        retdt = datetime.date(2000,01,01)
    return retdt

def string_to_date(inputstring):
    retdt = None   
    if (is_inputstring_valid(inputstring, CHROME_DATE_FORMAT)):
        logging.debug('Trying to convert #' + inputstring + '#: it seems a CHROME date...') 
        retdt = convert_date(inputstring, CHROME_DATE_FORMAT)
    elif (is_inputstring_valid(inputstring, IE10_DATE_FORMAT)): 
        logging.debug('Trying to convert #' + inputstring + '# it seems a IE10 date...') 
        retdt = convert_date(inputstring, IE10_DATE_FORMAT)
    else:
        logging.debug('Cannot convert date. Defaulting to 01/01/2000')
        retdt = datetime.date(2000,01,01)
    return retdt

def create_fable(dbfableuser):
    """ Create a new DbFable for user """
    logging.debug('Creating NEW DbFable for user ' + str(dbfableuser.nickname))
    the_fable = DbFable(parent=dbfableuser)
    the_fable.set_defaults()
    the_fable.put()
    return the_fable

def create_or_get_fable(user):
    """ Get the fable of the user if it exists, else create one.
        Returns a DBFable object. """
    dbfableuser = DbFableUser.get_from_user(user)
    afable = None
    if (dbfableuser):
        logging.debug('Found DbFable user ' + user.nickname())
        storedfable = DbFable.get_from_user(dbfableuser)
        if (storedfable):
            logging.debug('There is a fable for user ' + user.nickname())
            afable = storedfable
        else:
            logging.debug('No fable found for user ' + user.nickname() + '. Creating one.')
            afable = create_fable(dbfableuser)
    else:
        logging.debug('DbFable user NOT FOUND!')
        raise StandardError()
    return afable

class Steps():
    """ Assign template and DB values according to the Wizard step """
    
    def __init__(self, step):
        self.current_step = step
        self.template_keys = [ 
                              ['heroheroine', 'heroname', 'birthdate'],
                              ['sender', 'dedication'],
                              ['template', 'heroheroine', 'heroname', 'sender', 'dedication', 'birthdate']
                             ]
        
    def template_values(self, template_values, list_of_values):
        key = self.current_step - 1
        logging.debug('> Setting step '+str(self.current_step))
        logging.debug('> Template keys '+str(self.template_keys[key]))
        logging.debug('> List of values '+str(list_of_values))
        if len(list_of_values) == len(self.template_keys[key]):
            j = 0
            for item in self.template_keys[key]:
                template_values[item] = list_of_values[j]
                logging.debug(":" + item + " = " + str(list_of_values[j]))
                j += 1
        else:
            raise Exception('Template Values and List of Values do not match')
        for tk, tv in template_values.items():
                logging.debug(":TemplateValue => " + tk + " = " + str(tv))
        return template_values
            

class Fabulator():
    """ DbFable builder """
    
    def __init__(self, user):
        self.the_user = user
        if (self.the_user != None):
            self.the_fable = create_or_get_fable(user)
            logging.debug('Built fabulator with '+str(self.the_fable))
        
    def templatevalues(self, step):
        """ Delivers template values for the next step """       
        logging.debug('Building template values for step = ' + str(step))   
        template_values = {
            'nickname': self.the_user.nickname(),
            'logout_url':  users.create_logout_url("/"),
            'version': version()
        }
        if (step > 0): 
            step_setter = Steps(step)
            map_of_values = {
                             1: [self.hero_heroine(), self.the_fable.name, self.the_fable.birthdate],
                             2: [self.the_fable.sender, self.the_fable.dedication],
                             3: [self.the_fable.template, self.hero_heroine(), self.the_fable.name, self.the_fable.sender, 
                                 self.the_fable.dedication, self.the_fable.birthdate]
                             }
            template_values = step_setter.template_values(template_values, map_of_values[step])
        return template_values 
        
    def process(self, step, values, refresh):
        """ Saves the attributes for each step of the process """
        """ To do: step must be int """
        if (len(values) > 0):          
            self._loginfo(step, values, refresh)           
            if (refresh != ''):
                istep = int(step) + 1
                step = str(istep)
            if (step == '1'):
                self.the_fable.template = values[0]
                logging.debug('DbFable.template = ' + values[0])
            if (step == '2'):
                self.the_fable.sex = values[0]
                logging.debug('DbFable.sex = ' + values[0])            
                if (len(values) >= 2):
                    self.the_fable.name = values[1]
                    logging.debug('DbFable.name = ' + values[1])
                if (len(values) == 3):
                    self.the_fable.birthdate = string_to_date(values[2])
                    logging.debug('DbFable.birthdate = ' + values[2])
            elif (step == '3'):
                self.the_fable.sender = values[0]
                logging.debug('DbFable.sender = ' + values[0])          
                self.the_fable.dedication = values[1]
                logging.debug('DbFable.dedication = ' + values[1])                 
            self.the_fable.put()
        
    def hero_heroine(self):
        """ Returns the string 'hero' if the sex is M """
        heroheroine = 'heroine'
        if (self.the_fable.sex =='M'):
            heroheroine = 'hero'
        return heroheroine
        
    def close(self):
        """ Closes the instance by deleting the DbFable entity """
        self.the_fable.delete()
        
    def _loginfo(self, step, values, refresh):
        count = 0
        if (refresh == ''):
            logging.debug('Processing step ' + step )
        else:
            logging.debug('Refreshing step ' + step + ' Refresh = '+ refresh )       
        logging.debug( 'Values: ')
        for value in values:
            logging.debug(' => value ' + str(count) + '  = ' + value)
            count += 1
        
        
    

        