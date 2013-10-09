""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 fabulator.py
 
"""

# pylint: disable=C0301

import logging
import datetime
import fableme.utils as utils

from fableme.version import version
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser
from google.appengine.api import users

class Steps(object):
    """ Assign template and DB values according to the Wizard step """
    
    def __init__(self, step):
        self.current_step = step
        self.template_keys = [ 
                              ['heroheroine', 'heroname', 'birthdate'],
                              ['sender', 'dedication'],
                              ['fable', 'heroheroine']
                             ]
        
    def template_values(self, template_values, list_of_values):
        key = self.current_step - 1
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
            

class Fabulator(object):
    """ DbFable builder """
    
    def __init__(self, google_user, fable_id):
        """
            Constructs a Fabulator object.
            -google_user: the current google user
            -fable_id: the fable ID of the fable on DB
        """
        self.the_user = google_user
        if (self.the_user != None):
            if (fable_id == '-1'):
                self.the_fable = Fabulator.create_new_fable(self.the_user)
            else:
                self.the_fable = Fabulator.get_fable(self.the_user, fable_id)   
            logging.debug('Built fabulator with Fable #'+str(fable_id))
        
    def templatevalues(self, step):
        """ Delivers template values for the next step """       
        logging.debug('Building template values for step = ' + str(step))   
        template_values = {
            'fable_id': self.the_fable.id,
            'nickname': self.the_user.nickname(),
            'logout_url':  users.create_logout_url("/"),
            'version': version()
        }
        if (step > 0): 
            step_setter = Steps(step)
            map_of_values = {
                                 1: [self.hero_heroine(), self.the_fable.name, self.the_fable.birthdate],
                                 2: [self.the_fable.sender, self.the_fable.dedication],
                                 3: [self.the_fable, self.hero_heroine()]
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
            elif (step == '2'):
                self.the_fable.sex = values[0]           
                if (len(values) >= 2):
                    self.the_fable.name = values[1].title()
                if (len(values) == 3):
                    self.the_fable.birthdate = utils.string_to_date(values[2])
            elif (step == '3'):
                self.the_fable.sender = values[0]         
                self.the_fable.dedication = values[1]
            self.update_fable_on_db()                
            
    
    def update_fable_on_db(self):
        self.the_fable.modified = datetime.datetime.now()
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
    
    @staticmethod        
    def create_new_fable(google_user):
        """ Return a newly created DbFable """
        return DbFable.create(google_user)
    
    @staticmethod
    def get_fable(google_user, fable_id):
        """ 
            Get the db_fable of the user with the 
            given id if it exists, else create one.
        """
        dbfableuser = DbFableUser.get_from_user(google_user)
        afable = None
        if (dbfableuser):
            logging.debug('Found DbFable user ' + google_user.nickname())
            logging.debug('Looking for fable #' + str(fable_id))
            storedfable = DbFable.get_fable(google_user, fable_id)
            if (storedfable):
                logging.debug('Fable #' + str(fable_id) + ' found.')
                afable = storedfable
            else:
                logging.debug('Cannot find fable #'+ str(fable_id) +' for user ' + google_user.nickname() +'. Creating one.')
                afable = Fabulator.create_new_fable(google_user)
        else:
            logging.debug('DbFable user NOT FOUND!')
            raise StandardError()
        return afable
        
        
    

        