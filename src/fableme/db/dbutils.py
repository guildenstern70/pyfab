""" 
 FableMe.com
 A LittleLite Web Application
 
 dbutils.py

"""

import logging

from google.appengine.ext import ndb
from fableme.db.schema import DbFable
from fableme.db.schema import DbFableUser


def get_all_users():
    return DbFableUser.query()


def get_my_bought_fables(user_email):
    query = _get_all_fables(user_email)
    if query.get() is not None:
        query = query.filter(DbFable.ready == True)
        query = query.filter(DbFable.bought == True)
        query = query.order(-DbFable.created)
    return query


def get_all_ready_fables(user_email):
    query = _get_all_fables(user_email)
    if query.get() is not None:
        query = query.filter(DbFable.ready == True)
        query = query.filter(DbFable.bought == False)
        query = query.order(DbFable.created)
    return query


def delete_fable(user_email, fable_id):
    fable_key = DbFable.get_fable_key(user_email, int(fable_id))
    fable_key.delete()


def delete_all_saved_fables(user_email):
    query = _get_all_fables(user_email)
    if query.get() is not None:
        query = query.filter(DbFable.bought == False)
        ndb.delete_multi(query.fetch(keys_only=True))
    else:
        logging.debug('Nothing to delete...?')


def _get_all_fables(user_email):
    ancestor_key = ndb.Key('DbFableUser', user_email)
    query = DbFable.query(ancestor=ancestor_key)
    query.order(-DbFable.created)
    return query

