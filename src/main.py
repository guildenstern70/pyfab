""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 main.py
 
"""

import logging
import webapp2

import fableme.pages

logging.getLogger().setLevel(logging.DEBUG)                     
APPLICATION = webapp2.WSGIApplication(
                            [ ('/', fableme.pages.Index),
                              ('/create', fableme.pages.Create),
                              ('/step', fableme.pages.Step),
                              ('/book', fableme.pages.Book),
                              ('/howitworks', fableme.pages.HowItWorks),
                              ('/print', fableme.pages.Print),
                              ('/print/pdf', fableme.pages.PrintPDF),
                              ('/serve/([^/]+)?', fableme.pages.ServeHandler) ],
                            debug=True)


