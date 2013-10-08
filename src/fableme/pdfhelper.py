""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 pdfhelper.py
 
"""

import logging
import pdfgenerator.loader as loader

class PDF(object):
    """ PDF Helper class """
    
    def __init__(self, db_fable, contents):
        logging.debug('Initializing PDF object')
        self.dbfable = db_fable
        self.text_contents = contents
    
    def prepare_pdf(self, file_h):
        logging.debug('Preparing PDF...')
        fable_loader = loader.FableLoader(file_h, self.dbfable)
        fable_loader.setContents(self.text_contents)
        fable_loader.build()
