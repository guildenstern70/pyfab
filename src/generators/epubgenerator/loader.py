'''
FableGenerator
epubgenerator.loader.py

@author: Alessio Saltarin
'''

import fablepage
import os
import codecs
import logging
import sys

import fableme.utils as utils

from generators import chapter, templateloader

class EPubLoader(templateloader.TemplateLoader):
    
    def __init__(self, fable_id, lang, character, dedication):
        super(EPubLoader, self).__init__(fable_id, lang, character, dedication)
        
    def build(self):
        if self._buildFableFromFile():
            if len(self.paras) > 0:
                self.fable_doc = fablepage.EPubFableDoc(self._title, standalone=True)
                self.fable_doc.initialize(self._language.get_ISO())
                self._parseFile()
                self._addCover()
                self.fable_doc.addTitle(self._title, self._dedication)
                for chapter in self.chapters:
                    self._buildChapter(self.fable_doc, chapter)
            else:
                print 'CRITICAL Loader Error: empty contents.'
                raise
            self.fable_doc.build() 
            
    def _get_format(self):
        return '.epub'
    
    def get_images_path_to(self, filename):
        pics_folder = "F_PICS"
        if (self._character.sex == 'M'):
            pics_folder = "M_PICS"
        filepath_en = self._get_resources_path_lang()
        images_path = os.path.join(filepath_en, pics_folder)
        lang_code = self._language.language_code()
        if (lang_code != "EN"):
            finalpath_otherlang = os.path.normpath(os.path.join(filepath_en, lang_code))
            fullfilepath = os.path.join(finalpath_otherlang, pics_folder)
            path_to_file = os.path.join(fullfilepath, filename)
            if (os.path.isfile(path_to_file)):
                images_path = fullfilepath
        return os.path.join(images_path, filename)
            
    def __get_fable(self):
        return self.fable_doc
    
    def __get_epub_file(self):
        return self._ebook_file
    
    def _replace_tags(self):
        template_text = super(EPubLoader, self)._replace_tags()
        template_text = template_text.replace('<para alignment="left" fontsize="16">',
                                              '<span class="fableme1">')
        template_text = template_text.replace('<para alignment="center" fontsize="16">',
                                              '<span class="fableme1 fablemecenter">')
        template_text = template_text.replace('<para alignment="right" fontsize="16">',
                                              '<span class="fableme1 fablemeright">')
        template_text = template_text.replace('</para>', '</span>')
        return template_text 
            
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_epub_file, doc="""Get fable ePUB file path.""")
    
class GoogleEPubLoader(EPubLoader):
    
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
        
    def save(self, file_h):
        saved = True
        try:
            if (self.fable_doc):
                self.fable_doc.save_h(file_h)
            else:
                logging.debug('Failed to save EPUB: fable_doc is empty.')
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
        readOk = True
        try:
            template_googlepath = self._get_resources_path_to(self._template['template_text_file'])
            logging.debug('Reading from ' + template_googlepath + '...')
            fablefile = codecs.open(template_googlepath, "r", "utf-8")
            self._fabletemplate = unicode(fablefile.read())
            fablefile.close()
            logging.debug('Reading file done.')
        except:
            readOk = False
            logging.error('*** Error reading fable template...')
            logging.error('*** %s', sys.exc_info())
        return readOk
    


        