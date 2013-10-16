""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
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
                              ('/book', fableme.pages.Book),
                              ('/contacts', fableme.pages.Contacts),
                              ('/create', fableme.pages.Create),
                              ('/deletefable', fableme.commands.DeleteFable),
                              ('/howitworks', fableme.pages.HowItWorks),
                              ('/print', fableme.printer.Print),
                              ('/print/pdf', fableme.printer.PrintPDF),
                              ('/register', fableme.pages.Register),
                              ('/serve/([^/]+)?', fableme.pages.ServeHandler), 
                              ('/step', fableme.pages.Step) ],
                            debug=True)


