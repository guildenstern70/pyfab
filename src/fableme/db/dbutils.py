""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 dbutils.py

"""

from google.appengine.ext import db
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser

class Queries():
      
    @staticmethod     
    def get_all_users(): 
        return DbFableUser.all()
    
    @staticmethod
    def get_all_fables(google_user):
        user_db = DbFableUser.get_from_user(google_user)
        query = DbFable.all()
        query.ancestor(user_db)
        query.filter('user_email', google_user.email())
        query.order('-created')
        return query
    
    @staticmethod
    def get_all_ready_fables(google_user):
        query = Queries.get_all_fables(google_user)
        query.filter('ready', True)
        return query
    
    @staticmethod
    def get_universe_fables(google_user):
        user_db = DbFableUser.get_from_user(google_user)
        query = DbFable.all()
        query.ancestor(user_db)
        return query
    
    @staticmethod
    def delete_fable(google_user, fable_id):
        fable = DbFable.get_fable(google_user, fable_id)
        fable.delete()
        
    @staticmethod
    def delete_all_fables(google_user):
        fables = DbFable.all()
        fables.filter('user_email', google_user.email())
        db.delete(fables)
        
    