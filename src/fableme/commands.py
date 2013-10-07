""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 commands.py

"""

import webapp2
import logging
import fableme.db.dbutils as dbutils

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

class DeleteFable(webapp2.RequestHandler): 
    """ Delete a fable """
    
    @login_required
    def get(self):
        """ http get handler """
        google_user = users.get_current_user()
        fable_id = self.request.get('id')
        logging.debug('Command: deleting fable #'+ fable_id + '...')
        dbutils.Queries.delete_fable(google_user, long(fable_id))
        logging.debug('Fable #'+ fable_id +' deleted.')
        self.redirect('/myaccount')
        
        