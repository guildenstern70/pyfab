""" 
 
 FableGenerator
 
 templateloader.py
 
"""

import logging

from abc import abstractmethod
from generators import tagreplacer
from generators import languages, chapter

import codecs
import os.path
import sys
import fableme.db.booktemplates as fables
import fableme.utils as utils


class TemplateLoader(object):
    """
    A 'loader' class is a class that loads a template from a text file,
    replaces tags, and saves a formatted (PDF, ePub, HTML) document.
    
    A 'loader' takes in input a 'formatter' (see TextFormatter) to
    select the formatting technology to be used (ie: PDF, ePub)
    
    Example of use:
    
            template = loader.SimpleLoader(fable_id, tlang, character)
            template.build() 
            template.save()
    
    """
    def __init__(self, fable_id, lang, character, dedication):
        """
        Initialize the template loader
        - fable_id: Fable id
        - lang: Fable language
        - character: A character as in fableme/db/character.py
        """
        self._fable_id = fable_id
        self._set_variables(lang, character, dedication)
    
    @abstractmethod
    def build(self):
        return NotImplemented
    
    def save(self):
        saved = True
        try:
            if self.fable_doc:
                self.fable_doc.save(self._ebook_file)
            else:
                logging.error('*** ABORTING')
                saved = False
        except:
            saved = False
            logging.error('Error %s' % (str(sys.exc_info())))
        return saved 
    
    def _addCover(self):
        unix_name = self._filename[:-4] + '.jpg'
        cover_filepath = self.get_images_path_to(unix_name)
        self.fable_doc.addCover(cover_filepath)
    
    def _addChapter(self, paragraphs):
        new_chapter = chapter.FableChapter()
        new_chapter.title = paragraphs[0]
        for i in range(1,len(paragraphs)):
            new_chapter.addParagraph(paragraphs[i])
        self.chapters.append(new_chapter)

    def _buildChapter(self, fable, chapter):
        fable.addChapterTitle(chapter.title)
        for paragraph in chapter.paragraphs:
            fable.addParagraphOrImage(paragraph, self)
        fable.addPageBreak()
    
    def _parseFile(self):
        chapter_paragraphs = []
        chapter_nr = 1
        for paragraph in self.paras:
            if (self._language.is_beginning_of_chapter(paragraph)):
                if (len(chapter_paragraphs) > 0):
                    self._addChapter(chapter_paragraphs)
                    chapter_nr += 1
                    chapter_paragraphs = []
            chapter_paragraphs.append(paragraph)  
            
    def _replace_tags(self):
        template_text = self._fabletemplate
        # print '-- Raplacing tags in ' + self._language.language_code()
        replacer = tagreplacer.Replacer(self._fabletemplate, self._character, self._language.language_code())
        replacements = replacer.get_replacements()
        for tag, val in replacements.items():
            if ((val != None) and (len(val)>0)):
                template_text = template_text.replace(tag, val)
        self.paras = template_text.split('\n')
        return template_text 
    
    def _get_format(self):
        return NotImplemented
    
    def _buildFableFromFile(self):
        """
            1) Reads the file from _filename
            2) Replaces tags based on variables passed
            3) Builds paragraphs
            
            return True if the file was correctly read
        """
        fileReadOk = True
        fileFullPath = self._get_resources_path_to(self._filename)
        self._fabletemplate = self._readGenericTextFile(fileFullPath)
        if len(self._fabletemplate) > 0:
            filecontents = self._replace_tags()
            self.paras = filecontents.split('\n')
            # print '-- The file has ' + str(len(self.paras)) + ' paragraphs.'
        else:
            fileReadOk = False
        return fileReadOk        
    
    def _readGenericTextFile(self, filePath):
        filecontents = ""
        print '-- Reading file ' + filePath
        try:
            fileobj = codecs.open(filePath, "r", "utf-8")
            filecontents = unicode(fileobj.read())
            fileobj.close()
        except IOError:
            logging.error('*** Critical error opening %s' % filePath)
            logging.error('*** ', sys.exc_info())
        return filecontents
            
    def _get_resources_path(self):
        fable_dir = self._template['template_dir']
        lang_code = self._language.language_code()
        filepath = utils.BasicUtils.get_from_relative_resources(fable_dir)
        if (lang_code != "EN"):
            filepath = os.path.join(filepath, lang_code)
        return utils.BasicUtils.normalize_path(filepath)
    
    def _get_resources_path_to(self, filename):
        return os.path.join(self._get_resources_path(), filename)

    def _get_resources_path_lang(self):
        fable_dir = self._template['template_dir']
        filepath_en = utils.BasicUtils.get_from_relative_resources(fable_dir)
        finalpath = os.path.normpath(filepath_en)
        return finalpath
    
    def _set_language(self, filename, lang):
        return languages.Language(lang)
        
    def _set_variables(self, lang, character, dedication):
        self._language = self._set_language(self._fable_id, lang)
        self._template = fables.get_book_template(self._fable_id)
        self._filename = self._template['template_text_file']
        self._dedication = dedication
        self._ebook_file = utils.BasicUtils.get_output_path(self._filename[:-4] + '_' + self._language.language_code() + self._get_format())
        self._title = self._template[self._language.get_title_key()]
        self._character = character
        self.fable_doc = None
        self.chapters = []
