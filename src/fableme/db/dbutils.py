""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 dbutils.py

"""

from google.appengine.ext import db

from fableme.db.schema import DbFableUser

class Queries():
      
    @staticmethod     
    def get_all_users(): 
        #itemQuery = 'SELECT * FROM DbFableUser ORDER BY added DESC'          
        #return db.GqlQuery(itemQuery)
        return DbFableUser.all()
    
    @staticmethod     
    def get_nr_fables_of_user(google_user_key): 
        itemQuery = 'SELECT COUNT(*) FROM DbFable WHERE ANCESTOR IS :1 ORDER BY added DESC'
        query = db.GqlQuery(itemQuery, google_user_key)
        return query.get()
    