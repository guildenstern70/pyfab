"""
FableGenerator
languages.py

@author: Alessio Saltarin
"""

chapter_string_EN = "Chapter"
chapter_string_IT = "Capitolo"
chapter_string_RO = "Capitolul"
    
class Language(object):
    """
    Language class. Supported languages (passed in the constructor as identifiers):
    
    "EN" : English
    "IT" : Italian
    "RO" : Romanian 
    
    """
    
    def __init__(self, language):
        self.__set_language(language)
        
    def is_beginning_of_chapter(self, paragraph):
        is_chapter = False
        chapter_ident = self.__get_chapter_identifier()
        if ((paragraph.startswith(chapter_ident) or (paragraph.startswith('END-OF-FILE')))):
            is_chapter = True
        return is_chapter
    
    def language_code(self):
        return self.lang_code
    
    def get_title_key(self):
        title_key = 'title'
        if self.lang_code != 'EN':
            title_key += '_' + self.lang_code
        return title_key
    
    def get_ISO(self):
        iso_lang = 'en-US'
        if (self.lang_code == 'IT'):
            iso_lang = "it-IT"
        elif (self.lang_code == 'RO'):
            iso_lang = "ro-RO"
        return iso_lang
               
    def language(self):
        return self.lang
    
    def __set_language(self, language):
        self.lang_code = "EN"
        self.lang = "English"
        if (language.lower() == "it"):
            self.lang = "Italian"
            self.lang_code = "IT"
        elif (language.lower() == "ro"):
            self.lang = "Romanian"
            self.lang_code = "RO"
        
    def __get_chapter_identifier(self):
        identifier = chapter_string_EN
        if (self.lang_code == "IT"):
            identifier = chapter_string_IT
        elif (self.lang_code == "RO"):
            identifier = chapter_string_RO
        return identifier
            
        
        