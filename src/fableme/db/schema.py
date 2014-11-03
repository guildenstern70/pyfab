""" 
 FableMe.com
 A LittleLite Web Application
 
 schema.py

"""

# pylint: disable=R0904

import logging
import datetime
import character
import fableme.db.booktemplates as booktemplates

from google.appengine.ext import db

    
class DbFableUser(db.Model):
    """ DB Schema: DbFableUser """
    
    user = db.UserProperty(required=True)
    email = db.StringProperty(required=True)
    name = db.StringProperty()
    nickname = db.StringProperty()
    added = db.DateTimeProperty(auto_now_add=True)
    receivenews = db.BooleanProperty(default=True)
    
    def __nr_of_fables(self):
        _query = DbFable.all()
        _query.ancestor(self)
        _query.filter('user_email', self.email)
        nr = _query.count()
        logging.debug('User ' + self.nickname +' has ' + str(nr) + ' fables.')
        return nr
    
    nr_of_fables = property(__nr_of_fables, doc="""Gets the number of fables of a user.""")
    
    def __repr__(self):
        return "DbFableUser [user="+self.email+"]"
    
    @staticmethod
    def get_from_user(google_user):
        """ Get the user record """
        user_key = db.Key.from_path('DbFableUser', google_user.email())
        return db.get(user_key)
    
    @staticmethod
    def get_from_dbuser(db_user):
        """ Get the user record """
        user_key = db.Key.from_path('DbFableUser', db_user.email)
        logging.debug('Getting Db User Key from ' + db_user.email + ' = ' + str(user_key))
        return db.get(user_key)
    
    @staticmethod
    def createuser(user, uname, unick, ubdate, unews):
        """ Create a user record """
        usermail = user.email()
        userdb = DbFableUser(key_name = usermail, user = user, email = usermail, 
                             name = uname, nickname = unick, birthDate = ubdate, receivenews = unews)
        logging.debug('Adding user ' + usermail + ' to DB')
        userdb.put()
        
        
class DbFable(db.Model):
    """ DB Schema: DbFable """
    
    user_email = db.StringProperty(required=True)
    template_id = db.IntegerProperty() # Foreign key to booktemplates template_id
    sex = db.StringProperty()
    name = db.StringProperty()
    birthdate = db.DateProperty()
    sender = db.StringProperty()
    dedication = db.StringProperty()
    language = db.StringProperty(default="EN")
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now_add=True)
    ready = db.BooleanProperty(default=False)
    bought = db.BooleanProperty(default=False)
    purchased = db.DateTimeProperty()
    downlink_pdf = db.StringProperty()
    downlink_epub = db.StringProperty()
    
    def __id(self):
        return self.key().id()
    
    def __template(self):
        return booktemplates.get_book_template(self.template_id)
    
    def __title(self):
        return self.template['title']
    
    def __age(self):
        return character.Character.calculate_age(self.birthdate)
    
    def __character(self):
        return character.Character.from_fable_db(self)
    
    def __localized_title(self):
        lang_code = self.language.lower()
        locTitle = ""
        if (lang_code == 'it'):
            locTitle = self.template['title_IT']
        elif (lang_code == 'ro'):
            locTitle = self.template['title_RO']
        else:
            locTitle = self.template['title']
        return locTitle
    
    def __language_desc(self):
        lang_code = self.language.lower()
        lang_desc = 'Unknown'
        if (lang_code == 'it'):
            lang_desc = 'Italian'
        elif (lang_code == 'ro'):
            lang_desc = 'Romanian'
        else:
            lang_desc = 'English'
        return lang_desc
    
    def __recommandation(self):
        book = booktemplates.Book(self.template_id)
        sexonly = True
        if (self.is_age_mismatch()):
            sexonly = False
        return book.recommendation(sexonly)
                    
    id = property(__id, doc="""Gets current fable ID (long number).""")
    template = property(__template, doc="""Get the book template dictionary of attributes""")
    age = property(__age, doc="""Get the child age (diff between birthdate and now)""")
    title = property(__title, doc="""Get the fable title""")
    character = property(__character, doc="""Get the fable main character attributes""")
    recommendation = property(__recommandation, doc="""Get the fable recommendation""")
    language_desc = property(__language_desc, doc="""Get the fable language as a word""")
    localized_title = property(__localized_title, doc="""Get the localized fable title""")
        
    @staticmethod
    def get_fable(google_user, fable_id):
        """ Get the (first) fable of the given user """
        user_db = DbFableUser.get_from_user(google_user)
        fable = DbFable.get_by_id(fable_id, parent = user_db)
        return fable
    
    @staticmethod
    def create(google_user):
        """ Create a new DbFable for user """
        user_db = DbFableUser.get_from_user(google_user)
        logging.debug('Creating NEW DbFable for user ' + str(user_db.nickname))
        the_fable = DbFable(parent=user_db, user_email=user_db.email)
        the_fable.set_defaults()
        the_fable.put()
        return the_fable
    
    def set_defaults(self):
        self.sex = "M"
        self.name = ""
        self.birthdate = datetime.date(2005,01,01)
        self.sender = "From mom and dad"
        self.dedication = "With love"
        
    def get_full_dedication(self):
        return self.dedication+"***"+self.sender
        
    def is_age_mismatch(self):
        mismatch = False
        book_template = self.__template()
        if ( (self.__age() > book_template['age_recomm_max']) 
             or (self.__age() < book_template['age_recomm_min'])):
            mismatch = True
        return mismatch
    
    def is_sex_mismatch(self):
        mismatch = False
        sex_recomm = self.__template()['sex_recomm']
        if (sex_recomm != 'M' and sex_recomm != 'F'):
            mismatch = False
        elif (self.sex.lower() != sex_recomm.lower()):
            mismatch = True
        return mismatch
    
    def __repr__(self):
        return "DbFable [ID="+str(self.key())+"]"
    
    
    
    