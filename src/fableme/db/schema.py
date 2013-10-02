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
    
    def __repr__(self):
        return "DbFableUser [user="+self.email+"]"
    
    @staticmethod
    def get_from_user(user):
        """ Get the user record """
        user_key = db.Key.from_path('DbFableUser', user.email())
        return db.get(user_key)
    
    @staticmethod
    def get_from_dbuser(user):
        """ Get the user record """
        user_key = db.Key.from_path('DbFableUser', user.email)
        logging.debug('Getting Db User Key from ' + user.email + ' = ' + str(user_key))
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
    
    template = db.StringProperty()
    sex = db.StringProperty()
    name = db.StringProperty()
    birthdate = db.DateProperty()
    sender = db.StringProperty()
    dedication = db.StringProperty()
    
    @staticmethod
    def get_from_user(dbfableuser):
        """ Get the (first) fable of the given user """
        user_key = DbFableUser.get_from_dbuser(dbfableuser)
        query = DbFable(parent=user_key).all()
        return query.get() # The first fable found for that user
    
    def set_defaults(self):
        self.template = "Unknown"
        self.sex = "M"
        self.name = ""
        self.birthdate = datetime.date(2000,01,01)
        self.sender = ""
        self.dedication = "From Mom and Dad"
    
    def __repr__(self):
        return "DbFable [ID="+str(self.key())+"]"
    
    
    
    