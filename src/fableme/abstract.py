""" 
 FableMe.com
 A LittleLite Web Application
 
 abstract.py

"""

import webapp2
import logging
import webuser

from webapp2_extras import sessions
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fableme.version import version
from fableme.db.schema import DbFableUser


class FablePage(webapp2.RequestHandler):
    """ base class for all site pages """
    
    def __init__(self, request, response, template_filename, request_authentication=False):
        """ constructor """
        # Set self.request, self.response and self.app.
        self.initialize(request, response)
        # Base class initialization
        self.logged = None # Web User - login info
        self.template_values = {}
        self.req_auth = request_authentication
        # Session
        self.session_store = sessions.get_store(request=request)
        # Login
        self._initialize_login()
        # Template
        if (template_filename):
            self.template_path = 'templates/'+template_filename
        self._initialize_template()
        
    def _initialize_login(self):           
        try:
            login_email = self.session['user_email']
            self.logged = webuser.WebUser.fromEmail(login_email)
        except KeyError:
            self.logged = webuser.WebUser()
        if self.logged.is_logged:
            logging.debug('Logged in with ' + self.logged.email)
        else:
            logging.debug('User not logged in')
    
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        session = None
        if (self.session_store):
            session = self.session_store.get_session()
            logging.debug('Session found')
        else:
            logging.debug('Session store not found.')       
        return session
    
    def dispatch(self):
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    
    def render(self):
        """ default http response handler """
        if (self.req_auth):
            self._authenticate_user()
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
        user_db = DbFableUser.get_from_email(self.logged.email)
        if user_db == None:
            isondb = False
        return isondb
                    
    def _authenticate_user(self):
        """ Authenticate user on DB """
        if not self.logged.is_logged:
            self.redirect('/register')

    def _initialize_template(self):
        self.template_values = {
            'loginobj': self.logged,
            'isadmin': self.logged.isadmin,
            'version': version()
        }

