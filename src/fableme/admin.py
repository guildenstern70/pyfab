""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 admin.py

"""

import logging
import webapp2

from django.core.paginator import Paginator
from fableme.abstract import FablePage
from fableme.db.dbutils import Queries

ITEMS_TO_FETCH = 10

class Administration(FablePage):
    """ /admin/admin fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "admin.html")
        
class AdminUsers(FablePage):
    """ /admin/users fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "admin_users.html")
        
    def get(self, page=1):
        data = Queries.get_all_users()
        paginator = Paginator(data, ITEMS_TO_FETCH)
        if page > paginator.num_pages:
            page = paginator.num_pages
        elif page < 1:
            page = 1
        self.template_values['registered_users'] = paginator.page(page)
        self.template_values['pages'] = range(1,paginator.num_pages)
        self.template_values['page'] = page
        self.template_values['total_users'] = data.count()
        self.render()
        
        
        
class AdminFables(FablePage):
    """ /admin/fables fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "admin_fables.html")
        
    def get(self, page=1):
        data = Queries.get_universe_fables(self.the_user)
        paginator = Paginator(data, ITEMS_TO_FETCH)
        if page > paginator.num_pages:
            page = paginator.num_pages
        elif page < 1:
            page = 1
        self.template_values['fables'] = paginator.page(page)
        self.template_values['pages'] = range(1,paginator.num_pages)
        self.template_values['page'] = page
        self.template_values['total_users'] = data.count()
        self.render()
       
        
logging.getLogger().setLevel(logging.DEBUG)                     
ADMIN_APP = webapp2.WSGIApplication(
                            [ 
                              ('/admin/admin', Administration),
                              ('/admin/users', AdminUsers),
                              ('/admin/fables', AdminFables),
                            ],
                            debug=True)
