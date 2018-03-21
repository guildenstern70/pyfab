""" 
 FableMe.com
 A LittleLite Web Application
 
 schema.py

"""

# pylint: disable=R0904

import logging
import datetime
import character
import fableme.db.booktemplates as booktemplates

from google.appengine.ext import ndb


class DbFableReview(ndb.Model):
    """ DB Schema: Fable review from user """

    user_email = ndb.StringProperty(required=True)
    fable_template_id = ndb.IntegerProperty(required=True)
    stars = ndb.IntegerProperty(required=True)
    title = ndb.StringProperty(required=True)
    added = ndb.DateTimeProperty(auto_now_add=True)
    review = ndb.StringProperty(required=True)
    user_fullname = ndb.StringProperty(required=True)
    accepted = ndb.BooleanProperty(default=False)
    likes = ndb.IntegerProperty(default=0)
    likes_users = ndb.TextProperty()

    def did_i_like_it(self, my_mail):
        if self.likes < 1:
            return False
        likes_users = self.likes_users.split(';')
        if my_mail in likes_users:
            return True
        return False

    @classmethod
    def like_it(cls, review_id, user_mail):
        review_obj = ndb.Key(urlsafe=review_id).get()
        review_obj.likes = int(review_obj.likes) + 1
        if review_obj.likes_users is None:
            review_obj.likes_users = user_mail
        else:
            review_obj.likes_users = review_obj.likes_users + ';' + user_mail
        review_obj.put()
        return int(review_obj.likes)

    @staticmethod
    def create(user_mail, template_id):
        """ Create a new DbFable for user """
        review = DbFableReview.find_by_user(user_mail, template_id)
        if review is None:
            review = DbFableReview(fable_template_id=int(template_id))
            review.user_email = user_mail
            logging.debug('New Review created by ' + user_mail)
        else:
            logging.debug('Review existed: updating.')
        return review

    @staticmethod
    def find_by_template_id(template_id):
        query = DbFableReview.query(DbFableReview.fable_template_id == int(template_id))
        return query.filter(DbFableReview.accepted == True)

    @staticmethod
    def find_by_user(user_mail, template_id):
        query = DbFableReview.query(DbFableReview.user_email == user_mail)
        query = query.filter(DbFableReview.fable_template_id == int(template_id))
        return query.get()


class DbFableUser(ndb.Model):
    """ DB Schema: DbFableUser """
    
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty()
    added = ndb.DateTimeProperty(auto_now_add=True)
    isadmin = ndb.BooleanProperty(default=False)
    receivenews = ndb.BooleanProperty(default=True)
    token = ndb.StringProperty()

    @staticmethod
    def get_from_login(logged_user):
        """ Get the user record from login user """
        user_key = ndb.Key('DbFableUser', logged_user.email)
        return user_key.get()
    
    @staticmethod
    def get_from_email(email):
        """ Get the user record from email """
        user_key = ndb.Key('DbFableUser', email)
        return user_key.get()
    
    @staticmethod
    def create_from_login(logged_user, password):
        """ Create a user record """
        usermail = logged_user.email
        logging.debug('Request adding user from login: ' + usermail)
        DbFableUser.create(usermail, password)
            
    @staticmethod
    def create(useremail, pwd):
        user_key = ndb.Key(DbFableUser, useremail)
        userdb = user_key.get()
        if userdb is not None:
            logging.debug('User already existed. ')
            return False  # User already exists
        else:
            userdb = DbFableUser(key=user_key, email=useremail, password=pwd)
            logging.debug('Adding user ' + useremail + ' to DB...')
            userdb.put()
            logging.debug('User updated or added. ')
        return True

    @staticmethod
    def create_with_token(useremail, pwd, auth_token):
        user_key = ndb.Key(DbFableUser, useremail)
        userdb = user_key.get()
        if userdb is not None:
            logging.debug('User already existed. ')
            return False
        else:
            userdb = DbFableUser(key=user_key, email=useremail, password=pwd, token=auth_token)
            logging.debug('Adding user ' + useremail + ' to DB... (with token)')
            userdb.put()
            logging.debug('User updated or added. ')
        return True
        
    def remove_token(self, auth_token):
        token_removed = False
        if auth_token == self.token:
            logging.debug('Token verified. User is now authenticated.')
            self.token = None
            self.put()
            token_removed = True
        else:
            logging.debug('Token NOT verified.')
        return token_removed
    
    def __repr__(self):
        return "DbFableUser [email="+self.email+"]"
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)
        
        
class DbFable(ndb.Model):
    """ DB Schema: DbFable """
    
    template_id = ndb.IntegerProperty()  # Foreign key to booktemplates template_id
    sex = ndb.StringProperty()
    name = ndb.StringProperty()
    birthdate = ndb.DateProperty()
    sender = ndb.StringProperty()
    dedication = ndb.StringProperty()
    language = ndb.StringProperty(default="EN")
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now_add=True)
    ready = ndb.BooleanProperty(default=False)
    bought = ndb.BooleanProperty(default=False)
    purchased = ndb.DateTimeProperty()
    downlink_pdf = ndb.StringProperty()
    downlink_epub = ndb.StringProperty()
    
    def __id(self):
        return self.key.id()
    
    def __template(self):
        return booktemplates.get_book_template(self.template_id)
    
    def __title(self):
        return self.template['title']
    
    def __age(self):
        return character.Character.calculate_age(self.birthdate)
    
    def __character(self):
        return character.Character.from_fable_db(self)
    
    def __localized_title(self):
        lang_code = self.language.lower()
        if lang_code == 'it':
            localized_title = self.template['title_IT']
        elif lang_code == 'ro':
            localized_title = self.template['title_RO']
        else:
            localized_title = self.template['title']
        return localized_title
    
    def __language_desc(self):
        lang_code = self.language.lower()
        if lang_code == 'it':
            lang_desc = 'Italian'
        elif lang_code == 'ro':
            lang_desc = 'Romanian'
        else:
            lang_desc = 'English'
        return lang_desc
    
    def __recommandation(self):
        book = booktemplates.Book(self.template_id)
        sexonly = True
        if self.is_age_mismatch():
            sexonly = False
        return book.recommendation(sexonly)
                    
    id = property(__id, doc="""Gets current fable ID (long number).""")
    template = property(__template, doc="""Get the book template dictionary of attributes""")
    age = property(__age, doc="""Get the child age (diff between birthdate and now)""")
    title = property(__title, doc="""Get the fable title""")
    character = property(__character, doc="""Get the fable main character attributes""")
    recommendation = property(__recommandation, doc="""Get the fable recommendation""")
    language_desc = property(__language_desc, doc="""Get the fable language as a word""")
    localized_title = property(__localized_title, doc="""Get the localized fable title""")
     
    @staticmethod
    def get_fable_key(user_email, fable_id):
        return ndb.Key('DbFableUser', user_email, 'DbFable', int(fable_id))
           
    @staticmethod
    def get_fable(user_email, fable_id):
        """ Get the fable of the given user
            user_email = email of the user
            fable_id = int id of the entity """
        id_fable = int(fable_id)
        logging.debug('Looking for DbFable #' + str(fable_id))
        fable_key = ndb.Key('DbFableUser', user_email, 'DbFable', id_fable)
        fable = fable_key.get()
        if fable is not None:
            logging.debug('Found Fable #'+str(fable)+' with template = '+str(fable.template_id))
        return fable
    
    @staticmethod
    def create(user_email):
        """ Create a new DbFable for user """
        user_db = DbFableUser.get_from_email(user_email)
        logging.debug('Creating NEW DbFable for user ' + str(user_db.email))
        the_fable = DbFable(parent=user_db.key)
        the_fable.set_defaults()
        the_fable.put()
        logging.debug('New Fable created. ID='+str(the_fable.id))
        return the_fable
  
    def set_defaults(self):
        self.sex = "M"
        self.name = ""
        self.birthdate = datetime.date(2014, 01, 01)
        self.sender = "From mom and dad"
        self.dedication = "With love"
        
    def get_full_dedication(self):
        return self.dedication+"***"+self.sender
        
    def is_age_mismatch(self):
        mismatch = False
        book_template = self.__template()
        if self.__age() > book_template['age_recomm_max'] or (self.__age() < book_template['age_recomm_min']):
            mismatch = True
        return mismatch
    
    def is_sex_mismatch(self):
        mismatch = False
        sex_recomm = self.__template()['sex_recomm']
        if sex_recomm != 'M' and sex_recomm != 'F':
            mismatch = False
        elif self.sex.lower() != sex_recomm.lower():
            mismatch = True
        return mismatch
    
    def __repr__(self):
        return "DbFable [ID="+str(self.__id())+"]"
