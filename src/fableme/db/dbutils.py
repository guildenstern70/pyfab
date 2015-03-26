""" 
 FableMe.com
 A LittleLite Web Application
 
 dbutils.py

"""

import logging

from google.appengine.ext import ndb
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser


class Queries():
      
    @staticmethod     
    def get_all_users(): 
        return DbFableUser.query()
    
    @staticmethod
    def get_all_fables(user_email):
        ancestor_key = ndb.Key('DbFableUser', user_email)
        query = DbFable.query(ancestor=ancestor_key)
        query.order(-DbFable.created)
        return query
    
    @staticmethod
    def get_my_bought_fables(user_email):
        query = Queries.get_all_fables(user_email)
        if query.get() is not None:
            query = query.filter(DbFable.ready == True)
            query = query.filter(DbFable.bought == True)
            query = query.order(-DbFable.created)
        return query
    
    @staticmethod
    def get_all_ready_fables(user_email):
        query = Queries.get_all_fables(user_email)
        if query.get() is not None:
            query = query.filter(DbFable.ready == True)
            query = query.filter(DbFable.bought == False)
            query = query.order(DbFable.created)
        return query
    
    @staticmethod
    def delete_fable(user_email, fable_id):
        fable_key = DbFable.get_fable_key(user_email, int(fable_id))
        fable_key.delete()
        
    @staticmethod
    def delete_all_saved_fables(user_email):
        query = Queries.get_all_fables(user_email)
        if query.get() is not None:
            query = query.filter(DbFable.bought == False)
            ndb.delete_multi(query.fetch(keys_only=True))
        else:
            logging.debug('Nothing to delete...?')
        
    @staticmethod    
    def update_or_register_user(logged_in_user, password):
        logging.debug('Updating or registering user...')
        user_record = DbFableUser.get_from_login(logged_in_user)
        if user_record is None:
            logging.debug('User not found on DB: adding')
            DbFableUser.create_from_login(logged_in_user, password)
        else:
            if user_record.password != password:
                logging.debug('New password detected: changing it')
                user_record.password = password
                user_record.put()
