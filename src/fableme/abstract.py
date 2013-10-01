""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 abstract.py

"""

import webapp2

from google.appengine.ext.webapp import template
from google.appengine.api import users
from fableme.version import version

class FablePage(webapp2.RequestHandler):
    """ base class for all site pages """
    
    def render(self):
        """ default http response handler """
        self.response.out.write(
            template.render(self.template, self.template_values)
            )
    
    def get(self):
        """ default http get handler """
        self.initialize_user()
        self.render()
        
    def initialize_user(self):
        """ http get handler """
        self.the_user = users.get_current_user()
        self.login_url = users.create_login_url("/")
        if (self.the_user):
            self.user_nick = self.the_user.nickname()
            self.logout_url = users.create_logout_url("/")
            
    def __init__(self, request, response, template_filename):
        """ constructor """
        # Set self.request, self.response and self.app.
        self.initialize(request, response)
        # Base class initialization
        self.user_nick = None
        self.login_url = None
        self.logout_url = None
        self.the_user = None
        self.template_values = {
            'nickname': self.user_nick,
            'login_url': self.login_url,
            'logout_url':  self.logout_url,
            'version': version()
        }
        if (template_filename):
            self.template = 'templates/'+template_filename
