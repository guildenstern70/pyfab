""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 pages.py

"""

# pylint: disable=C0301


import urllib
import logging
import fableme.db.dbutils as dbutils

import fableme.fabulator as fabulator
import fableme.utils as utils

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp import template
from google.appengine.api import users

from fableme.version import version
from fableme.abstract import FablePage
from fableme.db.schema import DbFableUser


# Pages

class Index(FablePage):
    """ /index page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "index.html")
        
class Register(FablePage):
    """ /register page """
    
    def savedata(self, user):
        firstLastName = self.request.get('firstLastName')
        nickName = self.request.get('nickName')
        birthDate = self.request.get('birthDate')
        receiveNews = self.request.get('receiveNews')
        r_news = False
        if (receiveNews=='on'):
            r_news = True
        bdate = utils.string_to_date(birthDate)
        DbFableUser.createuser(user, firstLastName, nickName, bdate, r_news)
          
    def post(self):
        user = users.get_current_user()
        self.savedata(user)
        self.redirect('/')
        
    @login_required  
    def get(self):
        self.template_values['emailaddr'] = self.the_user.email()
        self.render() 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "register.html")
    
class Create(FablePage):
    """ /create fable page """
    
    @login_required  
    def get(self):
        if (self.user_db):
            self.template_values['nr_fables'] = self.user_db.nr_of_fables
            self.template_values['fables'] = dbutils.Queries.get_all_fables(self.the_user)
        self.template_values['return_page'] = 'create'
        self.render() 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "create.html", request_authentication=True)
        
class MyAccount(FablePage):
    """ /myaccount fable page """
    
    @login_required  
    def get(self):
        self.template_values['name'] = self.user_db.name
        self.template_values['nickname'] = self.user_db.nickname
        self.template_values['emailaddr'] = self.user_db.email
        self.template_values['birthdate'] = self.user_db.birthDate
        self.template_values['receivenews'] = self.user_db.receivenews
        self.template_values['return_page'] = 'myaccount'
        self.template_values['fables'] = dbutils.Queries.get_all_fables(self.the_user)
        self.render()
    
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
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        step = self.request.get('s') # steps, zero base (first step = 0)
        refresh = self.request.get('refresh') # if refresh has a value, the same step is refreshed
        values = self.request.get_all('value')
        fable = fabulator.Fabulator(self.the_user, long(fable_id)) 
        if (values != None):
            fable.process(step, values, refresh) # Save step data into FableDb
        target_page = 'templates/step' + step + '.html'
        logging.debug('Requesting page ' + target_page)
        self.response.out.write(
                template.render(target_page, fable.templatevalues(int(step)))
                )
           
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'create.html', request_authentication=True)
        
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
        nickname = self.request.get('nick')
        lastmod = self.request.get('lastmod')
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        pdf_file_name = 'Fable_' + nickname + '_' + lastmod + '.pdf'
        self.send_blob(blob_info, save_as=pdf_file_name)



        