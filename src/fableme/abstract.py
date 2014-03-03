""" 
 FableMe.com
 A LittleLite Web Application
 
 abstract.py

"""

import webapp2
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users
from fableme.version import version
from fableme.db.schema import DbFableUser


class FablePage(webapp2.RequestHandler):
    """ base class for all site pages """
    
    def render(self):
        """ default http response handler """
        if (self.req_auth):
            self._authenticate_user(self.the_user)
        self.response.out.write(
            template.render(self.template_path, self.template_values)
            )
        
    def get(self):
        """ default http get handler """
        self.render()
            
    def is_user_on_db(self):
        """ See if user is on db (asks DB every time).
            If you do not want to check DB another time,
            use if (self.user_db) """
        isondb = True
        self.user_db = self._get_user_from_db(self.the_user)
        if (self.user_db == None):
            isondb = False
        else:
            self.user_nick = self.user_db.nickname
        return isondb
        
    def _get_user_from_db(self, user):
        user_on_db = DbFableUser.get_from_user(user)
        if (user_on_db == None):
            logging.debug('User not found on DB. ')
        else:
            logging.debug('User is found on DB: ' + user_on_db.nickname)
        return user_on_db
                    
    def _authenticate_user(self, user):
        """ Authenticate user on DB """
        if (not self.is_user_on_db()):
            self.redirect('/register')

    def _initialize_user(self):
        self.the_user = users.get_current_user()
        self.login_url = users.create_login_url("/")
        if (self.the_user):
            self.user_db = self._get_user_from_db(self.the_user)
            if (self.user_db == None):
                self.user_nick = self.the_user.nickname()
            else:
                self.user_nick = self.user_db.nickname
            self.logout_url = users.create_logout_url("/")

    def _initialize_template(self):
        self._initialize_user()
        self.template_values = {
            'nickname': self.user_nick,
            'login_url': self.login_url,
            'logout_url':  self.logout_url,
            'isadmin': users.is_current_user_admin(),
            'version': version()
        }
              
    def __init__(self, request, response, template_filename, request_authentication=False):
        """ constructor """
        # Set self.request, self.response and self.app.
        self.initialize(request, response)
        # Base class initialization
        self.user_db = None  # User with data regitered on DB
        self.user_nick = None
        self.login_url = None
        self.logout_url = None
        self.the_user = None # User as registered in Google
        self.template_values = {}
        self.req_auth = request_authentication
        if (template_filename):
            self.template_path = 'templates/'+template_filename
        self._initialize_template()
