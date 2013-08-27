""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 pages.py

"""

# pylint: disable=C0301

import os
import urllib
import webapp2
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from fableme.fabulator import Fabulator
from fableme.writer import Writer
from fableme.version import version
from fableme.db.schema import DbFableUser


def register_user(user):
    """ Register user on DB """
    visitinguser = DbFableUser.get_from_user(user)
    if (visitinguser == None):
        logging.debug('User not found on DB. Adding. ')
        DbFableUser.createuser(user)
    else:
        logging.debug('User is found on DB: ' + str(visitinguser))


# Pages
class FablePage(webapp2.RequestHandler):
    """ base class for all site pages """
    
    def get(self):
        self.initialize_user()
        template_values = {
            'nickname': self.user_nick,
            'login_url': self.login_url,
            'logout_url':  self.logout_url,
            'version': version()
        }
        self.response.out.write(
                template.render(self.template, template_values)
                )
        
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
        if (template_filename):
            self.template = 'templates/'+template_filename
        
class Index(FablePage):
    """ /index page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "index.html")
    
class Create(FablePage):
    """ /create fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "create.html")
        
class HowItWorks(FablePage):
    """ /howitworks fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "howitworks.html")
    
class Step(FablePage):
    """ Handler for every /step page """  
    
    @login_required  
    def get(self):
        """ http get handler """
        self.initialize_user()
        register_user(self.the_user)
        step = self.request.get('s') # steps, zero base (first step = 0)
        refresh = self.request.get('refresh') # if refresh has a value, the same step is refreshed
        values = self.request.get_all('value')
        fable = Fabulator(self.the_user) 
        if (values != None):
            fable.process(step, values, refresh) # Save step data into FableDb
        target_page = 'templates/step' + step + '.html'
        logging.debug('Requesting page ' + target_page)
        self.response.out.write(
                template.render(target_page, fable.templatevalues(int(step)))
                )
           
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'create.html')
        
class Book(webapp2.RequestHandler):
    """ Handler for every /book page """ 
  
    @login_required
    def get(self):
        """ http get handler """
        book = self.request.get('bookid')
        # Book 0 -> Peter and the Pirates
        # Book 1 -> Anna goes to Aragon 
        template_values = {
            'version': version(),
            'title': 'My voyage to Aragon',
            'sku': 'SKU #83203',
            'bookimg': 'annatoaragon.jpg',
            'sidebar_pic': 'Anna.jpg',
            'desc_title': 'A dream comes true',
            'desc_desc': """This is the story of little Anna, a beautiful princess who travels 
                            to the land of Aragon and discovers that wisdom (knowledge) and wit
                            (perception and learning) are both needed in life. It is written 
                            with a medieval feel and as a rhyming ode. The story follows 
                            Anna who is riding to school on her pony and becomes distracted 
                            when they meet a fox. She, her pony and the fox begin a journey 
                            through the forest. As the princess progresses through the adventures 
                            she reflects after each one on the moral or learning point.""",
            
        }
        if (book == '0'):
            template_values = {
            'version': version(),
            'title': 'When I met the Pirates',
            'sku': 'SKU #83321',
            'bookimg': 'peterandpirates.jpg',
            'sidebar_pic': 'rustic_pirate.jpg',
            'desc_title': 'A great adventure...',
            'desc_desc': """This is a beautiful pirate story for boys and girls all over the world. 
                            The hero, Peter, joins an interesting crew made of a dog pirate, a cat pirate, a parrot pirate and a rat pirate. Toget
                            her they sail the sees and have a lot of fun.""",
            
            }
        target_page = 'templates/book.html'
        self.response.out.write(
                template.render(target_page, template_values)
                )
        
class Print(webapp2.RequestHandler):
    """ /print page """ 
    
    def _prepare(self, user):
        """ read the template and prepare for pdf creation """
        fable = Fabulator(user) 
        fable_sex = fable.the_fable.sex
        fable_title = fable.the_fable.template
        fable_name = fable.the_fable.name
        if fable_title == 'Peter and the pirates':
            filepath = os.path.join(os.path.split(__file__)[0], '../resources/Peter.txt')
        else:
            filepath = os.path.join(os.path.split(__file__)[0], '../resources/Anna.txt')
        fablefile = open(filepath, 'r')
        filecontents = fablefile.read()
        fablefile.close()
        self.fablewriter = Writer(filecontents, fable_title, fable_sex, fable_name)
    
    @login_required    
    def get(self):
        """ http get handler """
        user = users.get_current_user()
        self._prepare(user)
        template_values = {
            'version': version(),
            'fable_contents': self.fablewriter.get_fable(),
            'title': self.fablewriter.get_title()
            }
        target_page = 'templates/print.html'
        self.response.out.write(template.render(target_page, template_values))
        
class PrintPDF(Print):
    """ /print page """ 
    
    @login_required
    def get(self):
        """ http get handler """
        user = users.get_current_user()
        self._prepare(user)
        blobkey = self.fablewriter.get_pdf()
        template_values = {
            'version': version(),
            'downloadURL': '/serve/%s' % blobkey
            }
        target_page = 'templates/download.html'
        self.response.out.write(template.render(target_page, template_values))
        

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Download the PDF """
    
    @login_required
    def get(self, resource):
        """ http get handler """
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info, save_as='YourFable.pdf')



        