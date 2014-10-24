""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 fabulator.py
 
"""

# pylint: disable=C0301

import logging
import datetime
import fableme.utils as utils
import db.booktemplates

from fableme.version import version
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser
from google.appengine.api import users

class Steps(object):
    """ Assign template and DB values according to the Wizard step """
    
    def __init__(self, step):
        self.current_step = step
        self.template_keys = [ 
                              ['fable_template', 'language'],
                              ['heroheroine', 'heropicture_boy', 'heropicture_girl', 'birthdate'],
                              ['sender', 'dedication'],
                              ['template_title', 'heroheroine', 'sexagemismatch']
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
            'fable': self.the_fable,
            'nickname': self.the_user.nickname(),
            'logout_url':  users.create_logout_url("/"),
            'version': version()
        }
        if (step > 0): 
            step_setter = Steps(step)
            map_of_values = {
                                 1: [self.get_template(), self.the_fable.language ],
                                 2: [self.hero_heroine(), self.get_character_pic('M'), self.get_character_pic('F'), 
                                     self.the_fable.birthdate],
                                 3: [self.the_fable.sender, self.the_fable.dedication],
                                 4: [self.the_fable.template['title'], self.hero_heroine(), self.get_sex_or_age_mismatch()]
                            }
            template_values = step_setter.template_values(template_values, map_of_values[step])
        return template_values
    
    def get_template(self):
        template_id = self.the_fable.template_id
        book = db.booktemplates.Book(template_id)
        return book
    
    def get_character_pic(self, sex):
        book = self.the_fable.template
        character_img = book['prot_boy']
        if (sex=='F'):
            character_img = book['prot_girl']            
        return character_img
    
    def get_sex_or_age_mismatch(self):
        return (self.the_fable.is_age_mismatch() or self.the_fable.is_sex_mismatch())
        
    def process(self, step, values, refresh):
        """ Processes data in HTTP Request to be saved on DB
            Saves the attributes for each step of the process 
            To do: step should be int """
        if (len(values) > 0):          
            self._loginfo(step, values, refresh)           
            if (refresh != ''):
                istep = int(step) + 1
                step = str(istep)   
            if (step == '1'):
                self.the_fable.template_id = int(values[0])
            elif (step == '2'):
                self.the_fable.language = values[0]
            elif (step == '3'):
                self.the_fable.sex = values[0]           
                if (len(values) >= 2):
                    self.the_fable.name = values[1].title()
                if (len(values) == 3):
                    self.the_fable.birthdate = utils.GoogleUtils.string_to_date(values[2])
            elif (step == '4'):
                self.the_fable.sender = values[0]         
                self.the_fable.dedication = values[1]
                self.the_fable.ready = True
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
        
        
    

        