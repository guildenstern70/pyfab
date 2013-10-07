""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 writer.py
 
"""



from __future__ import with_statement
from collections import OrderedDict
from google.appengine.api import files

from fableme.pdfhelper import PDF
from fableme.tagreplacer import Replacer

import logging

def savetoblob(xbuffer):
    """ Save file to blob """
    file_name = files.blobstore.create('application/octet-stream')        
    with files.open(file_name, 'a') as memorypdf:
        memorypdf.write(xbuffer)
    files.finalize(file_name)
    return files.blobstore.get_blob_key(file_name)

class Writer(object):
    """ This class actually builds the fable """
    
    def __init__(self, template, title, sex, name):
        self.fable_title = title
        self.replacer = Replacer(template, sex, name)
        
    def get_title(self):
        return self.fable_title
        
    def get_fable(self):
        """ Get the final fable """
        for tag, val in self.replacer.get_replacements():
            self.fable_template = self.fable_template.replace(tag, val)
        return self.fable_template
    
    def get_chapters(self):
        """ Get a dictionary in the form { Chapter Title : Chapter body } """
        fable = self.get_fable()
        chapters = fable.split('Chapter')
        clean_chapters = OrderedDict()
        for chapter in chapters:
            first_newline = chapter.find('\n')
            first_fullstop = chapter.find('.')
            if first_fullstop > 0:
                chapter_title = chapter[first_fullstop+2:first_newline]
                chapter_body = chapter[first_newline:]
                clean_chapters[chapter_title] = chapter_body
        return clean_chapters
    
    def get_pdf(self):
        """ Returns a blobkey containing the fable in PDF format """
        logging.debug('Creating PDF')
        fable_chapters = self.get_chapters()
        pdf = PDF()
        pdf.set_title(self.fable_title)
        pdf.set_author('FableMe')
        j = 1
        for chapter_title, chapter_body in fable_chapters.items():
            logging.debug('Writing chapter ' + str(j))
            pdf.print_chapter(j, chapter_title, chapter_body)
            j += 1     
        xbuffer = pdf.output('fable.pdf', 'S')
        logging.debug('Saving to blob...')
        blobkey = savetoblob(xbuffer)
        logging.debug('... OK done. Blobkey = ' + str(blobkey))
        return blobkey



        
        