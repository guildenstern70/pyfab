
""" 
 FableMe.com
 A LittleLite Web Application
 
 pages.py

"""

# pylint: disable=C0301


import logging
import stripe
import random

import fableme.db.dbutils as dbutils
import fableme.db.schema as schema
import fableme.db.booktemplates as booktemplates
import fableme.fabulator as fabulator
import fableme.printer as printer
import fableme.webuser as webuser

from google.appengine.ext import deferred
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail
from fableme.abstract import FablePage
from fableme.db.schema import DbFableUser
from fableme.utils import BasicUtils
from email import email

# Pages

class Index(FablePage):
    """ /index page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "index.html")
    
TO_ADDRESS = 'info@fableme.com'
CCN_ADDRESSES = ['alessiosaltarin@gmail.com', 'sdi78@yahoo.com']
        
class Contacts(FablePage):
    """ /contacts page """
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "contacts.html")
        
    def get(self):
        self._x = random.randint(1, 10)
        self._y = random.randint(1, 10)
        self.template_values['x_num'] = self._x
        self.template_values['y_num'] = self._y
        self.template_values['xyxy'] = self._x + self._y
        self.render()
        
    def sendcontactmail(self, email, name, problem, message):
        from_field = name + ' <' + email + '>'
        body_field = message
        body_field += "\n================================="
        body_field += "\n Send answer to: "
        body_field += "\n " + from_field
        body_field += "\n================================="
        mail.send_mail(sender = "FableMe.com Support <support@fableomatic.appspotmail.com>",
                       to = TO_ADDRESS,
                       bcc = CCN_ADDRESSES,
                       subject = "[FABLEME - "+ problem +"] Support request from " + name,
                       body = body_field)
        
    def post(self):
        email_contact = self.request.get('contactEmail').strip()
        email_name = self.request.get('contactName').strip()
        email_problem = self.request.get('contactProblem').strip()
        email_message = self.request.get('mailMessage').strip()
        logging.debug('Sending contact mail')
        self.sendcontactmail(email_contact, email_name, email_problem, email_message)
        logging.debug('Done.')
        self.redirect('/contacts?sentmail=y')
        

class EditExisting(FablePage):
    """ /editexisting page """
     
    def get(self):
        if (self.user_db):
            self.template_values['nr_fables'] = self.user_db.nr_of_fables
            self.template_values['fables'] = dbutils.Queries.get_all_ready_fables(self.the_user)
        self.template_values['return_page'] = 'create'
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "editfable.html")
        
class Preview(FablePage):
    """ /preview page """
    
    def get(self):
        issuu_id = self.request.get('issuu') 
        self.template_values['issuu_id'] = issuu_id
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "issuu.html")
        
        
class ThankYouReg(FablePage):
    """ /thankyou page """
    
    def get(self):
        tokenized = self.request.get('tokenized') 
        if tokenized:
            self.template_values['tokenized'] = True
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "thankyouregistered.html")
        
class Register(FablePage):
    """ /register page """
    
    def create_new_user(self):
        token = str(random.randint(10000,99999))
        email = self.request.get('email')
        password = self.request.get('password')
        DbFableUser.create_with_token(email, password, token)
        self.sendconfirmationmail(email, token)
        
    def sendconfirmationmail(self, email_to, token):
        link = 'http://' + BasicUtils.get_production_domain() + '/register?token=' + token + '&mail=' + email_to
        body_field = """

Thank you for registering at FableMe.com

We have successfully received your membership registration and your personal profile has been created. 

In order to to activate your account you must verify your email address. 
Click here to verify your account: 
{{link}}
        
        """
        logging.debug('Mail link: ' + link)
        mail.send_mail(sender = "FableMe.com Support <support@fableomatic.appspotmail.com>",
                       to = email_to,
                       subject = "FableMe.com - Registration confirmation",
                       body = body_field.replace('{{link}}', link))
          
    def post(self):
        self.create_new_user()
        self.redirect('/thankyou')

    def get(self):
        token = self.request.get('token')
        email = self.request.get('mail')
        if token and email:
            user = DbFableUser.get_from_email(email)
            if user.remove_token(token):
                logging.debug('Token successfully removed.')
                self.session['user_email'] = email
            self.redirect('/thankyou?tokenized=1')
        else: 
            if self.logged.is_logged:
                self.redirect('/') # User is already logged in
            else:
                self.render() 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "signup.html")
        self.template_values['google_login'] = users.create_login_url()
        
 
class Login(FablePage):
    """ /login fable page """
    
    def performlogin(self, email, password):
        logging.debug('User '+ email +' wants to login: ')
        # Security check
        authorization = webuser.WebUser.authorize(email, password)
        if authorization == webuser.LoginResults.KO_EMAIL:
            self.redirect('/login?loginfailed=user')
        elif authorization == webuser.LoginResults.KO_PWD:
            self.redirect('/login?loginfailed=pwd')
        else:
            self.logged.login(email, (authorization == webuser.LoginResults.OK_ADMIN))
            self.session['user_email'] = email
            self.redirect('/') # User is logged in
        
    def performfblogin(self, email):
        logging.debug('FB Login Server Side')
        if email is not None:
            logging.debug('Trying to authenticate '+ email+ 'on DB...')
            user_db = schema.DbFableUser.get_from_email(email)
            if user_db is not None:
                logging.debug('OK, user found: added on ' + str(user_db.added))
                self.session['user_email'] = email
            else:
                logging.debug('User not found. I am registering it.')
                rndnumber = random.randint(1000,9999)
                user_db = schema.DbFableUser.create(email, 'qRT7x'+str(rndnumber))
                logging.debug('User created.')
            self.session['user_email'] = email
            self.redirect('/') # User is logged in
        else:
            logging.debug('FB Login without email: redirecting on register page')
            self.redirect('/register')
                     
    def performgooglelogin(self, google_user):
        logging.debug('User '+ google_user.nickname() +' wants to login from Google')
        self.session['user_email'] = str(google_user.email())
        self.redirect('/') # User is logged in
        
    def post(self):
        user_email = self.request.get("email")
        user_password = self.request.get("password")
        source = self.request.get("loginsource")
        if source == 'fb0':
            self.performfblogin(user_email)
        else:
            self.performlogin(user_email, user_password)
    
    def get(self):
        loginfailed = self.request.get("loginfailed")
        if loginfailed == 'user':
            self.template_values['unknownuser'] = True
        elif loginfailed == 'pwd':
            self.template_values['wrongpassword'] = True        
        user = users.get_current_user()
        if user:
            self.performgooglelogin(user) 
        else:    
            self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "signin.html", request_authentication=False)
        self.template_values['google_login'] = users.create_login_url()

        
class Logout(FablePage):
    """ /logout procedures """
    
    def __logout(self):
        self.logged.logout()
        self.session.pop('user_email', None)
        
    
    def googlelogout(self):
        user = users.get_current_user()
        self.__logout()
        if user:
            self.redirect(users.create_logout_url('/'))
    
    def passwordlogout(self):
        self.__logout()
        self.redirect('/')
        
    def get(self):
        user = users.get_current_user()
        if user:
            self.googlelogout()
        else:
            self.passwordlogout()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, None, request_authentication=True)
        

class AllFables(FablePage):
    """ /allfables fable page """
    
    def get(self):
        books = booktemplates.get_all_books()
        self.template_values['fables'] = books
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "allfables.html", request_authentication=False)
           
class Create(FablePage):
    """ /create fable page """
     
    def get(self):
        fables = dbutils.Queries.get_all_ready_fables(self.logged.email)
        self.template_values['nr_fables'] = fables.count()
        self.template_values['fables'] = fables
        self.template_values['return_page'] = 'create'
        self.render()
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "create.html", request_authentication=True)
        
class MyAccount(FablePage):
    """ /myaccount fable page """
     
    def get(self):
        if (self.request.get('updated') == '1'):
            self.template_values['updated'] = 'True'
        panel = self.request.get('panel')
        if len(panel) != 1:
            panel = "2"
        user_db = self.get_user_db()
        self.template_values['emailaddr'] = user_db.email
        self.template_values['added'] = user_db.added
        self.template_values['receivenews'] = user_db.receivenews
        self.template_values['return_page'] = 'myaccount?panel=2'
        self.template_values['panel'] = panel
        self.template_values['fables'] = dbutils.Queries.get_all_ready_fables(user_db.email)
        purchased_books = dbutils.Queries.get_my_bought_fables(user_db.email)
        self.template_values['bought_fables'] = purchased_books
        self.render()
        
    def post(self):
        user_db = self.get_user_db()
        if (self.request.get('receivenews') == 'on'):
            user_db.receivenews = True
        else:
            user_db.receivenews = False
        logging.debug('Updating user ' + user_db.email + ' to DB')
        user_db.put()
        self.redirect('/myaccount?updated=1&panel=1')
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "account.html")
        
class HowItWorks(FablePage):
    """ /howitworks fable page """
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, "howitworks.html")
    
class Step(FablePage):
    """ Handler for every /step page """  
    
    def get(self):
        """ http get handler """
        try:
            # the fable to edit (-1: new fable)
            fable_id = self.session['fable_id']
        except KeyError:
            fable_id = -1
        step = self.request.get('s') # steps, zero base (first step = 0)
        if int(step) == 0:
            fable_id = -1
        logging.debug('Step '+ str(step) + ' with ID='+str(fable_id))
        refresh = self.request.get('refresh') # if refresh has a value, the same step is refreshed
        values = self.request.get_all('value')
        fable = fabulator.Fabulator(self.logged.email, fable_id)
        self.session['fable_id'] = fable.the_fable.id 
        logging.debug('Saving session: fable_id='+ str(self.session['fable_id']))
        if (values != None):
            fable_id = fable.process(step, values, refresh) # Save step data into FableDb                
        target_page = 'templates/step' + step + '.html'
        template_vals = dict(self.template_values.items() + fable.templatevalues(int(step)).items())
        self.response.out.write(template.render(target_page, template_vals))
           
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'create.html', request_authentication=True)
        
class Book(FablePage):
    """ Handler for every /book page """ 
  
    def get(self):
        """ http get handler """
        book = self.request.get('bookid')
        book_obj = booktemplates.Book(int(book))     
        self.template_values['fable'] = book_obj
        self.template_values['templatesex'] = book_obj.default_sex
        self.template_values['book'] = book
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'book.html')
        
class HowEPub(FablePage):
    """ Handler for /howepub page """ 
  
    def get(self):
        """ http get handler """
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'howepub.html')

class Buy(FablePage):
    """ Handler for /buy page """ 

    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        fable = schema.DbFable.get_fable(self.logged.email, int(fable_id)) 
        fable_cover_gen = ""
        if fable.sex == 'M':
            fable_cover_gen = fable.template['bookimg_boy']
        else:
            fable_cover_gen = fable.template['bookimg_girl']
            
        if (fable.language != 'EN'):
            fable_cover_gen = fable_cover_gen[:-4] + '_' + fable.language + '.jpg'            
        self.template_values['fable'] = fable
        self.template_values['cover'] = fable_cover_gen
        self.template_values['template'] = fable.template
        self.template_values['templatesex'] = fable.sex
        self.template_values['user_email'] = self.logged.email
        self.template_values['ebook_price_cents'] = fable.template['price_eurocents']
        self.template_values['ebook_price_string'] = self._get_price_string(fable.template['price_eurocents'])
        self.render()
                
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'buy.html')
        
    def _get_price_string(self, price_in_cents):  
        price = price_in_cents / 100.0  
        return "{:10.2f} EUR".format(price)


class DeleteFable(FablePage): 
    """ Delete a fable """
    
    def get(self):
        """ http get handler """
        user_email = self.session['user_email']
        return_page = self.request.get('retpage')
        fable_id = self.request.get('id')
        if (fable_id != 'all'):
            dbutils.Queries.delete_fable(user_email, long(fable_id))
        else:
            dbutils.Queries.delete_all_saved_fables(user_email)
        self.redirect('/'+return_page)
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, None)        
        
        
class Order(FablePage):
    """ Handler for /buy page """ 
    
    def perform_stripe_order(self, token, customer_email, customer_fable_id):
        logging.debug('Beginning Stripe Order Management')
        
        order_complete = False
        
        # Stripe API Key
        stripe.api_key = "sk_test_vojAPjPK6uORgf8fGejCkuGQ"
         
        logging.debug('Token is ' + token)
         
        try:
            logging.debug('Charging credit card for user ' + customer_email)
            charge = stripe.Charge.create(
                  amount=499, # amount in cents, again
                  currency="eur",
                  card=token,
                  description="Your purchase at FableMe.com")
            order_complete = True
            logging.debug('Issued an order for ' + str(charge.amount/100.0) + charge.currency)
            logging.debug('Customer has succesfully purchased the Fable #' + customer_fable_id)
            logging.debug('Transaction done.')
        except stripe.CardError, e:
            body = e.json_body
            err  = body['error']
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Err type: %s" % err['type'] + " - Err code: %s" % err['code']
            logging.error('STRIPE ERROR:' + "Type is: %s" % err['type'] )
            logging.error('STRIPE ERROR:' + "Code is: %s" % err['code'] )
            logging.error('STRIPE ERROR:' + "Param is: %s" % err['param'])
            logging.error('STRIPE ERROR:' + "Message is: %s" % err['message'])
        except stripe.error.InvalidRequestError, e:
            logging.error('STRIPE ERROR: Invalid parameters were supplied to Stripe API')
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Invalid parameters were supplied to Stripe API"
        except stripe.error.AuthenticationError, e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            logging.error('STRIPE ERROR: Authentication with Stripe API failed')
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Invalid parameters were supplied to Stripe API"
        except stripe.error.APIConnectionError, e:
            # Network communication with Stripe failed
            logging.error('STRIPE ERROR: Network communication with Stripe failed')
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Network communication with Stripe failed"
        except stripe.error.StripeError, e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            logging.error('STRIPE ERROR: Generic stripe error')
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Generic stripe error"
        except Exception, e:
            # Something else happened, completely unrelated to Stripe
            logging.error('STRIPE ERROR: Generic error, non stripe')
            logging.exception(e) 
            self._errormsg1 = "Credit Card Transaction Error"
            self._errormsg2 = "Generic error"
            
        return order_complete
 
    
    def order_complete(self, fable_id, fable_format):
        printObj = printer.PrinteBook(self.logged.email)
        deferred.defer(printObj.printbook, fable_id, fable_format)
        
    def post(self):
        """ http post handler """
        logging.debug('Order post handler')
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        fable_format = self.request.get('fmt')
        token = self.request.get('stripeToken')
        logging.debug('Fable id > ' + fable_id)
        logging.debug('Stripe token > ' + token)
        logging.debug('Format > ' + fable_format)
        fableid = int(fable_id)
        fable = schema.DbFable.get_fable(self.logged.email, fableid) 
        self.template_values['template'] = fable.template
        self.template_values['templatesex'] = fable.sex
        
        if self.perform_stripe_order(token, self.logged.email, fableid):
            self.template_values['order_complete'] = True
            self.template_values['errormsg_1'] = '0'
            self.template_values['errormsg_1'] = '1'
            self.order_complete(fable_id, fable_format)   
        else:
            self.template_values['order_complete'] = False
            self.template_values['errormsg_1'] = self._errormsg1
            self.template_values['errormsg_1'] = self._errormsg2    
        self.render()
        
                
    def __init__(self, request, response):
        self._errormsg1 = ''
        self._errormsg2 = ''
        FablePage.__init__(self, request, response, 'orderplaced.html')



        