""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 writer.py
 
"""

from __future__ import with_statement
from collections import OrderedDict
from google.appengine.api import files
from fableme.pdfhelper import PDF

import logging

def savetoblob(xbuffer):
    """ Save file to blob """
    file_name = files.blobstore.create('application/octet-stream')        
    with files.open(file_name, 'a') as memorypdf:
        memorypdf.write(xbuffer)
    files.finalize(file_name)
    return files.blobstore.get_blob_key(file_name)

class Writer():
    """ This class actually builds the fable """
    
    def __init__(self, template, title, sex, name):
        self.fable_template = template
        self.fable_title = title
        self.character_sex = sex
        self.character_name = name
        self.tags = self._process_template()
        self.replacements_dict = self._build_dictionary()
        
    def get_title(self):
        return self.fable_title
        
    def get_fable(self):
        """ Get the final fable """
        for tag, val in self.replacements_dict.items():
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

    def _build_dictionary(self):
        tag_dict = {}
        for tag in self.tags:
            tag_dict[tag] = self._tag_replace(self.character_sex,tag)
        return tag_dict
    
    def _process_template(self):
        intag = False
        tag = ""
        tags_found = set()
        for ch in self.fable_template:
            if (ch == '<'):
                intag = True
            elif (ch == '>'):
                intag = False
                tags_found.add(tag+'>')
                tag = ""
            if (intag):
                tag += ch
        return tags_found
    
    def _tag_replace(self, sex, tag):
        """ A tag with underscore <his_her> is turned into 'his' if male, else 'her'
            A tag without underscore is processed turning the key into the value, ie.: <name> => 'Alessio' """
        replaced_word = ''
        underindex = tag.find('_')
        if underindex > 0:
            if (sex == 'F'): 
                replaced_word = tag[1:underindex] 
            else:
                replaced_word = tag[underindex+1:-1]
        else:
            if (tag == '<name>'):
                replaced_word = self.character_name
        return replaced_word

        
        