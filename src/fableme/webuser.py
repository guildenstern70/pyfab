import logging

from fableme.db.schema import DbFableUser
from fableme.db.dbutils import Queries


class WebUser(object):
    
    def __init__(self):
        self.__logged = False
        self.__nickname = ''
        self.__name = ''
        self.__email = ''
        self.__isadmin = False
    
    def __is_logged(self):
        return self.__logged
    
    def __set_logged(self, value):
        self.__logged = value
        
    def __update_or_create_on_db(self):
        Queries.update_or_register_user(self)
        
    def login(self, name, nickname, email, isadmin):
        self.__email = email
        self.__name = name
        self.__nickname = nickname
        self.__logged = True
        self.__isadmin = isadmin
        self.__update_or_create_on_db()
        
    def login_from_google(self, google_user, isadmin):
        self.__email = google_user.email()
        self.__name = google_user.nickname()
        self.__nickname = google_user.nickname()
        self.__isadmin = isadmin
        self.__logged = True
        self.__update_or_create_on_db()
        
    def logout(self):
        self.__email = ''
        self.__name = ''
        self.__nickname = ''
        self.__logged = False
        self.__isadmin = False
         
    @property
    def email(self):
        return self.__email
    
    @property
    def name(self):
        return self.__name
    
    @property
    def isadmin(self):
        return self.__isadmin
    
    @property
    def nick(self):
        return self.__nickname
    
    def __repr__(self):
        return 'WebUser '+ self.__nickname + ' ('+ self.__email + ')'
    
    @classmethod   
    def fromEmail(self, user_email):
        logging.debug('Checking user: '+user_email)
        dbuser = DbFableUser.get_from_email(user_email)
        webuser = WebUser()
        if dbuser != None:
            logging.debug('User found on DB!')
            webuser.login(dbuser.name, dbuser.nickname, user_email, dbuser.isadmin)
        else:
            logging.debug('User NOT found on DB. Using empty webuser')
        return webuser
      
    def get_db_user(self):
        return DbFableUser.get_from_email(self.__email)
           
    is_logged = property(__is_logged, __set_logged,
                     doc="""Gets or sets if the user is logged.""")
    
    