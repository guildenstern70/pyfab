"""
FableGenerator
fablegenerator.loader.py

@author: Alessio Saltarin
"""

from generators import chapter, templateloader

import sys
import codecs
import os.path
import fablepage
import fableme.utils as utils
import logging

  
class SimpleLoader(templateloader.TemplateLoader):
    
    def __init__(self, fable_id, lang, character, dedication):
        super(SimpleLoader, self).__init__(fable_id, lang, character, dedication)
    
    def build(self):
        if self._buildFableFromFile():
            if len(self.paras) > 0:
                self.fable_doc = fablepage.PdfFableDoc(self._title, standalone=True)
                self._parseFile()
                self._addCover()
                self.fable_doc.addTitle(self._title, self._dedication)
                for xchapter in self.chapters:
                    self._buildChapter(self.fable_doc, xchapter)
            else:
                print 'CRITICAL Loader Error: empty contents.'
                raise
            self.fable_doc.build() 
                
    def get_images_path_to(self, filename):
        pics_folder = "F_PICS"
        if self._character.sex == 'M':
            pics_folder = "M_PICS"
        filepath_en = self._get_resources_path_lang()
        images_path = os.path.join(filepath_en, pics_folder)
        lang_code = self._language.language_code()
        if lang_code != "EN":
            finalpath_otherlang = os.path.normpath(os.path.join(filepath_en, lang_code))
            fullfilepath = os.path.join(finalpath_otherlang, pics_folder)
            path_to_file = os.path.join(fullfilepath, filename)
            if os.path.isfile(path_to_file):
                images_path = fullfilepath
        return os.path.join(images_path, filename)
    
    def _get_format(self):
        return '.pdf'
                                                                
    def __get_fable(self):
        return self.fable_doc
    
    def __get_pdf_file(self):
        return self._ebook_file
        
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_pdf_file, doc="""Get fable PDF file path.""")
    
    
class GoogleLoader(SimpleLoader):
    
    @classmethod
    def from_fable_db(cls, dbfable):
        fable_template_id = dbfable.template_id
        lang = dbfable.language
        character = dbfable.character
        dedication = dbfable.get_full_dedication()
        return cls(fable_template_id, lang, character, dedication)       
    
    def load_template(self):
        self._read_file_template()
        return self._replace_tags()

    def build(self):
        if len(self.paras) > 0:
            self.fable_doc = fablepage.PdfFableDoc(self._title, standalone=False)
            self._parseFile()
            self._addCover()
            self.fable_doc.addTitle(self._title, self._dedication)
            for chapter in self.chapters:
                self._buildChapter(self.fable_doc, chapter)
        else:
            logging.error('CRITICAL PDF Error: empty contents.')
            raise
        self.fable_doc.build()
    
    def save(self, file_h):
        saved = True
        try:
            if self.fable_doc:
                self.fable_doc.save(file_h)
            else:
                logging.warn('Aborting PDF save: fable_doc is null.')
                saved = False
        except:
            saved = False
        return saved
    
    def get_resources_path_to(self, filename):
        filename = os.path.join(self._get_resources_path(), filename) 
        return utils.GoogleUtils.get_from_google(filename)
        
    def get_template(self):
        return self._template_file
    
    def _read_file_template(self):
        read_ok = True
        try:
            template_googlepath = self._get_resources_path_to(self._template['template_text_file'])
            logging.debug('Reading from ' + template_googlepath + '...')
            fablefile = codecs.open(template_googlepath, "r", "utf-8")
            self._fabletemplate = unicode(fablefile.read())
            fablefile.close()
            logging.debug('Reading file done.')
        except:
            read_ok = False
            logging.error('*** Error reading fable template...')
            logging.error('*** %s', sys.exc_info())
        return read_ok
    

