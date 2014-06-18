""" 
 FableMe.com
 A LittleLite Web Application
 
 pages.py

"""

# pylint: disable=C0301


import logging
import time

import fableme.db.dbutils as dbutils
import fableme.db.schema as schema
import fableme.db.booktemplates as booktemplates
import fableme.fabulator as fabulator
import fableme.utils as utils
import fableme.printer as printer

from google.appengine.ext import deferred
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp import template
from google.appengine.api import users

from fableme.abstract import FablePage
from fableme.db.schema import DbFableUser


# Pages

class Index(FablePage):
    """ /index page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "index.html")
        
class Contacts(FablePage):
    """ /contacts page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "contacts.html")
        
class EditExisting(FablePage):
    """ /editexisting page """
    
    @login_required  
    def get(self):
        if (self.user_db):
            self.template_values['nr_fables'] = self.user_db.nr_of_fables
            self.template_values['fables'] = dbutils.Queries.get_all_ready_fables(self.the_user)
        self.template_values['return_page'] = 'create'
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "editfable.html")
        
class Preview(FablePage):
    """ /preview page """
    
    def get(self):
        issuu_id = self.request.get('issuu') 
        self.template_values['issuu_id'] = issuu_id
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "issuu.html")
        
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
        bdate = utils.GoogleUtils.string_to_date(birthDate)
        DbFableUser.createuser(user, firstLastName, nickName, bdate, r_news)
          
    def post(self):
        user = users.get_current_user()
        self.savedata(user)
        self.redirect('/')
        
    @login_required  
    def get(self):
        if (self.user_db):
            self.redirect('/')
        else:
            self.template_values['emailaddr'] = self.the_user.email()
            self.render() 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "register.html")
 
class AllFables(FablePage):
    """ /allfables fable page """
    
    def get(self):
        books = booktemplates.get_all_books()
        self.template_values['fables'] = books
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "allfables.html", request_authentication=False)
           
class Create(FablePage):
    """ /create fable page """
    
    @login_required  
    def get(self):
        if (self.user_db):
            self.template_values['nr_fables'] = self.user_db.nr_of_fables
            self.template_values['fables'] = dbutils.Queries.get_all_ready_fables(self.the_user)
        self.template_values['return_page'] = 'create'
        self.render() 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "create.html", request_authentication=True)
        
class MyAccount(FablePage):
    """ /myaccount fable page """
    
    @login_required  
    def get(self):
        if (self.request.get('updated') == '1'):
            self.template_values['updated'] = 'True'
        panel = self.request.get('panel')
        if len(panel) != 1:
            panel = "2"
        self.template_values['name'] = self.user_db.name
        self.template_values['nickname'] = self.user_db.nickname
        self.template_values['emailaddr'] = self.user_db.email
        self.template_values['added'] = self.user_db.added
        self.template_values['receivenews'] = str(self.user_db.receivenews)
        self.template_values['return_page'] = 'myaccount?panel=2'
        self.template_values['panel'] = panel
        self.template_values['fables'] = dbutils.Queries.get_all_ready_fables(self.the_user)
        self.template_values['bought_fables'] = dbutils.Queries.get_my_bought_fables(self.the_user)
        self.render()
        
    def post(self):
        self.user_db.name = self.request.get('name')
        self.user_db.nickname = self.request.get('nickname')
        if (self.request.get('receivenews') == 'on'):
            self.user_db.receivenews = True
        else:
            self.user_db.receivenews = False
        logging.debug('Updating user ' + self.user_db.nickname + ' to DB')
        self.user_db.put()
        self.redirect('/myaccount?updated=1&panel=1')
    
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
        book_obj = booktemplates.Book(int(book))     
        self.template_values['fable'] = book_obj
        self.template_values['templatesex'] = book_obj.default_sex
        self.template_values['book'] = book
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'book.html')
        
class Buy(FablePage):
    """ Handler for /buy page """ 
    
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        fable = schema.DbFable.get_fable(self.the_user, long(fable_id)) 
        fable_cover_gen = ""
        if fable.sex == 'M':
            fable_cover_gen = fable.template['bookimg_boy']
        else:
            fable_cover_gen = fable.template['bookimg_girl']
        fable_cover_gen = fable_cover_gen[:-4] + '_' + fable.language + '.jpg' 
        self.template_values['fable'] = fable
        self.template_values['cover'] = fable_cover_gen
        self.template_values['template'] = fable.template
        self.template_values['templatesex'] = fable.sex
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'buy.html')
        
        
class Order(FablePage):
    """ Handler for /buy page """ 
    
    def order_complete(self, fable_id, fable_format):
        printObj = printer.PrinteBook(self.the_user)
        deferred.defer(printObj.printBook, fable_id, fable_format)
        time.sleep(2)
        # Send mail
        
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        fable_format = self.request.get('fmt')
        fable = schema.DbFable.get_fable(self.the_user, long(fable_id)) 
        self.template_values['template'] = fable.template
        self.template_values['templatesex'] = fable.sex
        self.order_complete(fable_id, fable_format)     
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'orderplaced.html')



        