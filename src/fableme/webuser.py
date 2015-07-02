"""

 FableMe.com
 A LittleLite Web Application

 webuser.py

"""

import logging
from fableme.db.schema import DbFableUser


class LoginResults(object):
    OK = 1
    OK_ADMIN = 2
    KO_EMAIL = -10
    KO_PWD = -100


class WebUser(object):
    
    def __init__(self):
        self.__logged = False
        self.__email = ''
        self.__isadmin = False
    
    def __is_logged(self):
        return self.__logged
    
    def __set_logged(self, value):
        self.__logged = value
            
    @staticmethod    
    def authorize(email, password):
        logging.debug('Authorizing user: ' + email)
        user_db = DbFableUser.get_from_email(email)
        if user_db is None:
            logging.debug('Unknown user')
            return LoginResults.KO_EMAIL
        if user_db.password != password:
            logging.debug('User known, but wrong password')
            return LoginResults.KO_PWD
        if user_db.isadmin:
            return LoginResults.OK_ADMIN
        return LoginResults.OK
        
    def login(self, email, isadmin):
        self.__email = email
        self.__logged = True
        self.__isadmin = isadmin
        
    def login_from_google(self, google_user, isadmin):
        self.__email = google_user.email()
        self.__isadmin = isadmin
        self.__logged = True
        user_db = DbFableUser.get_from_email(self.__email)
        if user_db is None:
            logging.debug('User not found: creating one.')
            DbFableUser.create(self.__email, 'ggl5x82393')
        
    def logout(self):
        self.__email = ''
        self.__logged = False
        self.__isadmin = False
        
    def nick(self):
        return WebUser.nick_from_email(self.__email)
         
    @property
    def email(self):
        return self.__email
    
    @property
    def isadmin(self):
        return self.__isadmin
    
    def __repr__(self):
        return 'WebUser ' + self.__email
    
    @staticmethod
    def nick_from_email(email):
        at_index = email.index('@')
        nick = email[0:at_index] + '_' + email[at_index+1:]
        return nick
            
    @classmethod   
    def from_email(cls, user_email):
        logging.debug('Checking user: '+user_email)
        dbuser = DbFableUser.get_from_email(user_email)
        webuser = WebUser()
        if dbuser is not None:
            logging.debug('User found on DB!')
            webuser.login(user_email, dbuser.isadmin)
        else:
            logging.debug('User NOT found on DB. Using empty webuser')
        return webuser
      
    def get_db_user(self):
        return DbFableUser.get_from_email(self.__email)
           
    is_logged = property(__is_logged, __set_logged,
                         doc="""Gets or sets if the user is logged.""")
