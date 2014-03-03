""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 pdfhelper.py
 
"""

from google.appengine.api import files

import logging
import pdfgenerator.loader as loader

class PdfProxy(object):
    """ PdfProxy Helper class """
    
    def __init__(self, db_fable):
        self.dbfable = db_fable
        self.fable_loader = loader.GoogleLoader.from_fable_db(self.dbfable)
        
    def load_template(self):
        logging.debug('Loading Template...')
        return self.fable_loader.load_template()
        
    def prepare_pdf(self):
        logging.debug('Preparing Pdf...')
        self.fable_loader.build()
           
    def save_pdf(self):
        """ Returns a blobkey containing the fable in PDF format """
        logging.debug('Saving to blob...')
        blobkey = self._save_to_blob()
        logging.debug('... OK done. Blobkey = ' + str(blobkey))
        return blobkey
    
    def _save_to_blob(self):
        file_name = files.blobstore.create('application/octet-stream')  
        with files.open(file_name, 'a') as blob_store_file:
            self.fable_loader.save(blob_store_file)
        files.finalize(file_name)
        return files.blobstore.get_blob_key(file_name)
              
        
