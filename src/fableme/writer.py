""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 writer.py
 
"""

from __future__ import with_statement  # WARNING: MUST BE FIRST LINE

import logging
import fableme.utils as utils
import fableme.db.booktemplates as booktemplates

from google.appengine.api import files
from fableme.pdfhelper import PdfProxy


class Writer(object):
    """ This class actually builds the fable, replacing tags from template,
        then creates PDF and saves it to blob store """
    
    def __init__(self, db_fable):
        self.dbfable = db_fable
        self.fable_contents = ""
        self.pdf_object = None
          
    def get_title(self):
        book = self.get_template()
        return book['title']
    
    def get_template(self):
        return booktemplates.get_book_template(self.dbfable.template_id)
    
    def prepare_pdf(self):
        """ Returns a string containing the actual fable """
        logging.debug('Creating PDF')
        self._read_file_template()
        self.pdf_object = PdfProxy(self.dbfable, self.fable_contents)
        self.pdf_object.prepare_pdf()  
        return self.pdf_object.contents   
        
    def save_pdf(self):
        """ Returns a blobkey containing the fable in PDF format """
        logging.debug('Saving to blob...')
        blobkey = self._save_to_blob()
        logging.debug('... OK done. Blobkey = ' + str(blobkey))
        return blobkey
    
    def _save_to_blob(self):
        file_name = files.blobstore.create('application/octet-stream')  
        with files.open(file_name, 'a') as blob_store_file:
            self.pdf_object.save_pdf(blob_store_file)
        files.finalize(file_name)
        return files.blobstore.get_blob_key(file_name)
    



        
        