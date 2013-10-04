""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 main.py
 
"""


import logging
import webapp2

import fableme.pages
import fableme.printer

logging.getLogger().setLevel(logging.DEBUG)                     
APPLICATION = webapp2.WSGIApplication(
                            [ ('/', fableme.pages.Index),
                              ('/create', fableme.pages.Create),
                              ('/myaccount', fableme.pages.MyAccount),
                              ('/create', fableme.pages.Create),
                              ('/register', fableme.pages.Register),
                              ('/step', fableme.pages.Step),
                              ('/book', fableme.pages.Book),
                              ('/howitworks', fableme.pages.HowItWorks),
                              ('/print', fableme.printer.Print),
                              ('/print/pdf', fableme.printer.PrintPDF),
                              ('/serve/([^/]+)?', fableme.pages.ServeHandler) ],
                            debug=True)


