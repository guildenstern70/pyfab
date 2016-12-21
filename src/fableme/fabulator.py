""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 fabulator.py
 
"""

# pylint: disable=C0301

import logging
import datetime
import fableme.utils as utils
import fableme.db.booktemplates

from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser


class Steps(object):
    """ Assign template and DB values according to the Wizard step """

    def __init__(self, step):
        self.current_step = step
        self.template_keys = [
            ['fable_template', 'language'],
            ['heroheroine', 'heroname', 'heropicture_boy', 'heropicture_girl', 'birthdate'],
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

    def __init__(self, user_email, fable_id):
        """
            Constructs a Fabulator object.
            -google_user: the current google user
            -fable_id: the fable ID of the fable on DB
        """
        self.the_user = DbFableUser.get_from_email(user_email)
        if self.the_user is not None:
            if fable_id < 0:
                self._createnewfable(user_email)
            else:
                self._getexistingfable(user_email, fable_id)

    def _createnewfable(self, user_email):
        self.the_fable = Fabulator.create_new_fable(user_email)
        logging.debug('A new fable has been created and saved')

    def _getexistingfable(self, user_email, fable_id):
        self.the_fable = Fabulator.get_fable(user_email, fable_id)
        if self.the_fable is None:
            self._createnewfable(user_email)
        else:
            logging.debug('A saved fable has been retrieved. Fable #' + str(fable_id))

    def templatevalues(self, step):
        """ Delivers template values for the next step """
        template_values = {
            'fable': self.the_fable
        }
        if step > 0:
            step_setter = Steps(step)
            map_of_values = {
                1: [self.get_template(), self.the_fable.language],
                2: [self.hero_heroine(), self.the_fable.name, self.get_character_pic('M'), self.get_character_pic('F'),
                    self.the_fable.birthdate],
                3: [self.the_fable.sender, self.the_fable.dedication],
                4: [self.the_fable.template['title'], self.hero_heroine(), self.get_sex_or_age_mismatch()]
            }
            template_values = step_setter.template_values(template_values, map_of_values[step])
        elif step == 0:
            fableme_fables = fableme.db.booktemplates.get_fableme_books()
            classic_fables = fableme.db.booktemplates.get_classic_books()
            template_values = {
                'fable': self.the_fable,
                'fableme_books': fableme.db.booktemplates.get_leftright_books(fableme_fables),
                'classic_books': fableme.db.booktemplates.get_leftright_books(classic_fables)
            }
        return template_values

    def get_template(self):
        template_id = self.the_fable.template_id
        book = fableme.db.booktemplates.Book(template_id)
        return book

    def get_character_pic(self, sex):
        book = self.the_fable.template
        character_img = book['prot_boy']
        if sex == 'F':
            character_img = book['prot_girl']
        return character_img

    def get_sex_or_age_mismatch(self):
        return self.the_fable.is_age_mismatch() or self.the_fable.is_sex_mismatch()

    def process(self, step, values, refresh):
        """ Processes data in HTTP Request to be saved on DB
            Saves the attributes for each step of the process 
            Return: the ID of the fable processed or created """
        if len(values) > 0:
            Fabulator._loginfo(step, values, refresh)
            if refresh != '':
                istep = int(step) + 1
                step = str(istep)
            if step == '1':
                self.the_fable.template_id = int(values[0])
            elif step == '2':
                self.the_fable.language = values[0]
            elif step == '3':
                if len(values) == 2:
                    self.the_fable.name = values[0].title()
                    self.the_fable.birthdate = utils.GoogleUtils.string_to_date(values[1])
                elif len(values) == 3:
                    self.the_fable.sex = values[0]
                    self.the_fable.name = values[1].title()
                    self.the_fable.birthdate = utils.GoogleUtils.string_to_date(values[2])
            elif step == '4':
                self.the_fable.sender = values[0]
                self.the_fable.dedication = values[1]
                self.the_fable.ready = True
            self.update_fable_on_db()
            return self.the_fable.id

    def update_fable_on_db(self):
        self.the_fable.modified = datetime.datetime.now()
        self.the_fable.put()
        logging.debug('Fable Saved: ' + str(self.the_fable))

    def hero_heroine(self):
        """ Returns the string 'hero' if the sex is M """
        heroheroine = 'heroine'
        if self.the_fable.sex == 'M':
            heroheroine = 'hero'
        return heroheroine

    def close(self):
        """ Closes the instance by deleting the DbFable entity """
        self.the_fable.delete()

    @staticmethod
    def _loginfo(step, values, refresh):
        count = 0
        if refresh == '':
            logging.debug('Processing step ' + step)
        else:
            logging.debug('Refreshing step ' + step + ' Refresh = ' + refresh)
        logging.debug('Values: ')
        for value in values:
            logging.debug(' => value ' + str(count) + '  = ' + value)
            count += 1

    @staticmethod
    def create_new_fable(user_email):
        """ Return a newly created DbFable """
        return DbFable.create(user_email)

    @staticmethod
    def get_fable(user_email, fable_id):
        """ 
            Get the db_fable of the user with the 
            given id if it exists, else create one.
            fable_id = int id of the fable
        """
        dbfableuser = DbFableUser.get_from_email(user_email)
        afable = None
        if dbfableuser:
            logging.debug('Found DbFable user ' + dbfableuser.email)
            logging.debug('Looking for fable #' + str(fable_id))
            storedfable = DbFable.get_fable(user_email, fable_id)
            if storedfable:
                logging.debug('Fable #' + str(fable_id) + ' found.')
                afable = storedfable
            else:
                logging.debug(
                    'Cannot find fable #' + str(fable_id) + ' for user ' + dbfableuser.email)
        else:
            logging.debug('DbFable user NOT FOUND!')
        return afable
