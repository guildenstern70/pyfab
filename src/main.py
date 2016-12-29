""" 
 
 FableMe.com 
 A LittleLite Web Application
 (c) 2013-15
 
 main.py
 
"""

import logging
import webapp2
import fableme.pages
import fableme.services
import fableme.printer

config = {'webapp2_extras.sessions': {
 'secret_key': 'bludream',
}}

logging.getLogger().setLevel(logging.DEBUG)
APPLICATION = webapp2.WSGIApplication(
    [('/', fableme.pages.Index),
     ('/myaccount', fableme.pages.MyAccount),
     ('/allfables', fableme.pages.AllFables),
     ('/book', fableme.pages.Book),
     ('/buy', fableme.pages.Buy),
     ('/changepassword', fableme.pages.ChangePassword),
     ('/contacts', fableme.pages.Contacts),
     ('/create', fableme.pages.Create),
     ('/deletefable', fableme.pages.DeleteFable),
     ('/editexisting', fableme.pages.EditExisting),
     ('/forgotpwd', fableme.pages.ForgotPassword),
     ('/howitworks', fableme.pages.HowItWorks),
     ('/howtoreadepub', fableme.pages.HowEPub),
     ('/likeit', fableme.services.LikeItHandler),
     ('/order', fableme.pages.Order),
     ('/preview', fableme.pages.Preview),
     ('/print', fableme.printer.Print),
     ('/print/book', fableme.pages.GetFreeBook),
     ('/register', fableme.pages.Register),
     ('/review', fableme.pages.Review),
     ('/serve/([^/]+)?', fableme.printer.ServeHandler),
     ('/thankyou', fableme.pages.ThankYouReg),
     ('/login', fableme.pages.Login),
     ('/logout', fableme.pages.Logout),
     ('/step', fableme.pages.Step)],
    debug=True, config=config)


