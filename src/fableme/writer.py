""" 
 
 FableMe.com 
 A LittleLite Web Application
 
 writer.py
 
"""

from __future__ import with_statement  # WARNING: THIS MUST BE FIRST LINE

import logging
import fableme.db.booktemplates as booktemplates

from fableme.generatorhelper import GeneratorProxy


class Writer(object):
    """ This class actually builds the fable, replacing tags from template,
        then creates the ebook and saves it to blob store """
    
    def __init__(self, db_fable):
        self.dbfable = db_fable
        self.fable_contents = ""
        self.ebook_object = None
          
    def get_title(self):
        book = self.get_template()
        return book['title']
    
    def get_template(self):
        return booktemplates.get_book_template(self.dbfable.template_id)
    
    def prepare(self, ebook_format):
        """ Returns a string containing the actual fable """
        logging.debug('Creating PDF')
        self._read_file_template()
        self.ebook_object = GeneratorProxy(self.dbfable, ebook_format, self.fable_contents)
        self.ebook_object.prepare_ebook()  
        return self.ebook_object.contents   
     
    



        
        