""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 generatorhelper.py
 
"""

import os
import logging
import generators.pdfgenerator.loader as pdf_loader
import generators.epubgenerator.loader as epub_loader
import cloudstorage as gcs

from google.appengine.ext import blobstore
from google.appengine.api import app_identity


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
           
    def save_ebook(self, filename):
        """ Saves the fable in PDF format """
        logging.debug('Saving to blob...')
        savedfile = self._save_to_cloud_store(filename)
        logging.debug('... OK done. Filename = ' + savedfile)
        return savedfile

    """ OLD BLOBSTORE SAVE
    def _save_to_blob(self):
        file_name = files.blobstore.create('application/octet-stream')  
        with files.open(file_name, 'a') as blob_store_file:
            self.fable_loader.save(blob_store_file)
        files.finalize(file_name)
        return files.blobstore.get_blob_key(file_name) """

    def _save_to_cloud_store(self, filename):
        logging.info("Saving file " + filename + " to GCS.")
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name + '/'
        filename = bucket + filename
        logging.info("File path is: " + filename)
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        with gcs.open(filename,
                      'w',
                      content_type='application/octet-stream',
                      retry_params=write_retry_params) as gcs_file:
            self.fable_loader.save(gcs_file)
        # Blobstore API requires extra /gs to distinguish against blobstore files.
        blobstore_filename = '/gs' + filename
        # This blob_key works with blobstore APIs that do not expect a
        # corresponding BlobInfo in datastore.
        return blobstore.create_gs_key(blobstore_filename)
