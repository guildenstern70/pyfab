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
        self.dbfable = db_fable
        self.fable_loader = loader.FableLoader(self.dbfable)
        self.text_contents = contents
    
    def prepare_pdf(self):
        logging.debug('Preparing PDF...')
        self.fable_loader.setContents(self.text_contents)
        self.fable_loader.build()
        
    def save_pdf(self, file_h):
        logging.debug('Saving PDF...')
        self.fable_loader.save(file_h)
        
        
