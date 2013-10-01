""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 pages.py

"""

# pylint: disable=C0301

import urllib
import logging

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp import template
from fableme.fabulator import Fabulator
from fableme.db.schema import DbFableUser
from fableme.version import version
from fableme.abstract import FablePage


def register_user(user):
    """ Register user on DB """
    visitinguser = DbFableUser.get_from_user(user)
    if (visitinguser == None):
        logging.debug('User not found on DB. Adding. ')
        DbFableUser.createuser(user)
    else:
        logging.debug('User is found on DB: ' + str(visitinguser))


# Pages

class Index(FablePage):
    """ /index page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "index.html")
    
class Create(FablePage):
    """ /create fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "create.html")
        
class MyAccount(FablePage):
    """ /myaccount fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "account.html")
        
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
        
class Book(FablePage):
    """ Handler for every /book page """ 
  
    @login_required
    def get(self):
        """ http get handler """
        book = self.request.get('bookid')
        # Book 0 -> Peter and the Pirates
        # Book 1 -> Anna goes to Aragon 
        book_template = {
            'title': 'My voyage to Aragon',
            'sku': 'SKU #83203',
            'bookimg': 'cover_voyage.jpg',
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
            book_template = {
                'version': version(),
                'title': 'When I met the Pirates',
                'sku': 'SKU #83321',
                'bookimg': 'cover_pirates.jpg',
                'sidebar_pic': 'rustic_pirate.jpg',
                'desc_title': 'A great adventure...',
                'desc_desc': """This is a beautiful pirate story for boys and girls all over the world. 
                                The hero, Peter, joins an interesting crew made of a dog pirate, a cat pirate, 
                                a parrot pirate and a rat pirate. Together they sail the sees and have 
                                a lot of fun.""",
                
                }
            
        self.template_values = dict(book_template.items() + self.template_values.items())
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'book.html')
        

        

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Download the PDF """
    
    @login_required
    def get(self, resource):
        """ http get handler """
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info, save_as='YourFable.pdf')



        