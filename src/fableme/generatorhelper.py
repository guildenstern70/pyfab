""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 generatorhelper.py
 
"""

from google.appengine.api import files

import logging
import generators.pdfgenerator.loader as pdf_loader
import generators.epubgenerator.loader as epub_loader

class GeneratorProxy(object):
    """ Generator Helper class """
    
    def __init__(self, ebook_format, db_fable):
        """
        format: "PDF" or "EPUB"
        db_fable: fable to be generated
        """
        self.dbfable = db_fable
        self.fable_loader = pdf_loader.GoogleLoader.from_fable_db(self.dbfable)
        if ebook_format.upper() == "EPUB":
            self.fable_loader = epub_loader.GoogleEPubLoader.from_fable_db(self.dbfable)
        
    def load_template(self):
        logging.debug('Loading Template...')
        return self.fable_loader.load_template()
        
    def prepare_ebook(self):
        logging.debug('Preparing eBook...')
        self.fable_loader.build()
           
    def save_ebook(self):
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
              
        
