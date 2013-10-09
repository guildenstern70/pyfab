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
        model = DbFableUser.all()
        return model
    
    @staticmethod
    def get_all_fables(google_user):
        user_db = DbFableUser.get_from_user(google_user)
        model = DbFable.all()
        model.ancestor(user_db)
        model.filter('user_email', google_user.email())
        return model
    
    @staticmethod
    def get_universe_fables(google_user):
        user_db = DbFableUser.get_from_user(google_user)
        model = DbFable.all()
        model.ancestor(user_db)
        return model
    
    @staticmethod
    def delete_fable(google_user, fable_id):
        fable = DbFable.get_fable(google_user, fable_id)
        fable.delete()
        
    @staticmethod
    def delete_all_fables(google_user):
        fables = DbFable.all()
        fables.filter('user_email', google_user.email())
        db.delete(fables)
        
    