""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 schema.py

"""

# pylint: disable=R0904

import logging
import datetime


from google.appengine.ext import db

class DbFableUser(db.Model):
    """ DB Schema: DbFableUser """
    
    user = db.UserProperty(required=True)
    email = db.StringProperty(required=True)
    name = db.StringProperty()
    nickname = db.StringProperty()
    birthDate = db.DateProperty()
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
        logging.debug('  => Name: ' + uname)
        logging.debug('  => Nick: ' + unick)
        logging.debug('  => BDay: ' + str(ubdate))
        logging.debug('  => News: ' + str(unews))
        userdb.put()
        
        
class DbFable(db.Model):
    """ DB Schema: DbFable """
    
    user_email = db.StringProperty(required=True)
    template = db.StringProperty()
    sex = db.StringProperty()
    name = db.StringProperty()
    birthdate = db.DateProperty()
    sender = db.StringProperty()
    dedication = db.StringProperty()
    
    def __id(self):
        return self.key().id()
       
    def __unix_name(self):
        return self.template.replace(' ', '_')
    
    def __template_text_file(self):
        return self.__unix_name() + '.txt'
    
    def __cover_file(self):
        return self.__unix_name() + '.jpg'
        
    id = property(__id, doc="""Gets fable ID (long number).""")
    unix_name = property(__unix_name, doc="""Gets fable title with underscores instead of spaces.""")
    template_filename = property(__template_text_file, doc="""Gets the name of the file containing the template.""")
    cover_filename = property(__cover_file, doc="""Gets the name of the file containing the cover image.""")
    
    @staticmethod
    def get_first_fable(google_user):
        """ Get the (first) fable of the given user """
        query = DbFable.get_all_fables(google_user)
        return query.get() # The first fable found for that user
    
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
    
    @staticmethod
    def get_all_fables(google_user):
        """ Get the (first) fable of the given user """
        user_db = DbFableUser.get_from_user(google_user)
        return DbFable(parent=user_db, user_email=user_db.email).all()
    
    def set_defaults(self):
        self.template = "Unknown"
        self.sex = "M"
        self.name = ""
        self.birthdate = datetime.date(2000,01,01)
        self.sender = ""
        self.dedication = "From Mom and Dad"
    
    def __repr__(self):
        return "DbFable [ID="+str(self.key())+"]"
    
    
    
    