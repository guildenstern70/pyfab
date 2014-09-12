""" 
 
 FableMe.com 
 A LittleLite Web Application
 (c) 2013-14
 
 main.py
 
"""


import logging
import webapp2

import fableme.pages
import fableme.commands
import fableme.printer

logging.getLogger().setLevel(logging.DEBUG)                     
APPLICATION = webapp2.WSGIApplication(
                            [ ('/', fableme.pages.Index),
                              ('/myaccount', fableme.pages.MyAccount),
                              ('/allfables', fableme.pages.AllFables),
                              ('/book', fableme.pages.Book),
                              ('/buy', fableme.pages.Buy),
                              ('/contacts', fableme.pages.Contacts),
                              ('/create', fableme.pages.Create),
                              ('/deletefable', fableme.commands.DeleteFable),
                              ('/editexisting', fableme.pages.EditExisting),
                              ('/howitworks', fableme.pages.HowItWorks),
                              ('/order', fableme.pages.Order),
                              ('/preview', fableme.pages.Preview),
                              ('/print', fableme.printer.Print),
                              ('/print/book', fableme.printer.PrinteBook),
                              ('/register', fableme.pages.Register),
                              ('/serve/([^/]+)?', fableme.printer.ServeHandler), 
                              ('/step', fableme.pages.Step) ],
                            debug=True)


