""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 writer.py
 
"""

from __future__ import with_statement  # WARNING: MUST BE FIRST LINE

import logging
import fableme.utils as utils

from google.appengine.api import files
from fableme.pdfhelper import PDF
from fableme.tagreplacer import Replacer

def savetoblob(pdf_object):
    """ Save file to blob """
    file_name = files.blobstore.create('application/octet-stream') 
    pdf_object.prepare_pdf()       
    with files.open(file_name, 'a') as blob_store_file:
        pdf_object.save_pdf(blob_store_file)
    files.finalize(file_name)
    return files.blobstore.get_blob_key(file_name)

class Writer(object):
    """ This class actually builds the fable, replacing tags from template,
        then creates PDF and saves it to blob store """
    
    def __init__(self, db_fable):
        self.dbfable = db_fable
          
    def get_title(self):
        return self.dbfable.template
        
    def get_fable(self):
        """ Get the final fable as a long string """
        logging.debug('Reading file template...')
        template = self._read_file_template()
        logging.debug('Replacing tags...')
        replacer = Replacer(template, self.dbfable.sex, self.dbfable.name)
        replacements = replacer.get_replacements()
        for tag, val in replacements.items():
            if ((val != None) and (len(val)>0)):
                template = template.replace(tag, val)
        return template
    
    def _read_file_template(self):
        template_googlepath = utils.get_from_resources(self.dbfable.template_filename)
        logging.debug('Reading from ' + template_googlepath + '...')
        fablefile = open(template_googlepath, 'r')
        filecontents = fablefile.read()
        fablefile.close()
        logging.debug('Reading file done.')
        return filecontents
    
    def get_pdf(self):
        """ Returns a blobkey containing the fable in PDF format """
        logging.debug('Creating PDF')
        pdf_contents = self.get_fable()
        pdf = PDF(self.dbfable, pdf_contents)
        logging.debug('Saving to blob...')
        blobkey = savetoblob(pdf)
        logging.debug('... OK done. Blobkey = ' + str(blobkey))
        return blobkey



        
        