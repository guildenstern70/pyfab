""" 
 
 FableMe.com 
 A LittleLite Web Application
 (c) 2013-14
 
 main.py
 
"""

import logging
import webapp2

import fableme.pages
import fableme.printer

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'bludream',
}

logging.getLogger().setLevel(logging.DEBUG)
APPLICATION = webapp2.WSGIApplication(
    [('/', fableme.pages.Index),
     ('/myaccount', fableme.pages.MyAccount),
     ('/allfables', fableme.pages.AllFables),
     ('/book', fableme.pages.Book),
     ('/buy', fableme.pages.Buy),
     ('/contacts', fableme.pages.Contacts),
     ('/create', fableme.pages.Create),
     ('/deletefable', fableme.pages.DeleteFable),
     ('/editexisting', fableme.pages.EditExisting),
     ('/howitworks', fableme.pages.HowItWorks),
     ('/howtoreadepub', fableme.pages.HowEPub),
     ('/order', fableme.pages.Order),
     ('/preview', fableme.pages.Preview),
     ('/print', fableme.printer.Print),
     ('/print/book', fableme.printer.PrinteBook),
     ('/register', fableme.pages.Register),
     ('/serve/([^/]+)?', fableme.printer.ServeHandler),
     ('/thankyou', fableme.pages.ThankYouReg),
     ('/login', fableme.pages.Login),
     ('/logout', fableme.pages.Logout),
     ('/step', fableme.pages.Step)],
    debug=True, config=config)


