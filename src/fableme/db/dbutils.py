""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 dbutils.py

"""

from google.appengine.ext import db


class Queries():
      
    @staticmethod     
    def get_all_users(): 
        itemQuery = 'SELECT * FROM DbFableUser ORDER BY added DESC'          
        return db.GqlQuery(itemQuery)
    