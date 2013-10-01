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
        
    def get(self):
        self.initialize_user()
        data = Queries.get_all_users()
        paginator = Paginator(data, ITEMS_TO_FETCH)
        
        
class AdminFables(FablePage):
    """ /admin/fables fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "admin_fables.html")
       
        
logging.getLogger().setLevel(logging.DEBUG)                     
ADMIN_APP = webapp2.WSGIApplication(
                            [ 
                              ('/admin/admin', Administration),
                              ('/admin/users', AdminUsers),
                              ('/admin/fables', AdminFables),
                            ],
                            debug=True)
