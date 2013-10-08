""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 dbutils.py

"""

from google.appengine.ext import db

from fableme.db.schema import DbFableUser
from fableme.db.schema import DbFable

class Queries():
      
    @staticmethod     
    def get_all_users(): 
        return DbFableUser.all()
    
    @staticmethod     
    def get_nr_fables_of_user(google_user_key): 
        itemQuery = 'SELECT COUNT(*) FROM DbFable WHERE ANCESTOR IS :1 ORDER BY added DESC'
        query = db.GqlQuery(itemQuery, google_user_key)
        return query.get()
    
    @staticmethod
    def delete_fable(google_user, fable_id):
        fable = DbFable.get_fable(google_user, fable_id)
        fable.delete()
        
    @staticmethod
    def delete_all_fables(google_user):
        fables = DbFable.all()
        fables.filter('user_email', google_user.email())
        db.delete(fables)
        
    