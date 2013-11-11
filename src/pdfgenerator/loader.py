'''
PDFGenerator
loader.py

@author: Alessio Saltarin
'''

import fablepage
import chapter
import logging
import fableme.utils as utils
import fableme.db.booktemplates as booktemplates

class FableLoader(object):
    
    def __init__(self, db_fable):
        book = booktemplates.get_book_template(db_fable.template_id)
        self._title = book['title']
        self.coverfilename = book['cover_image']
        self.fable_doc = None
        self.chapters = []
              
    def setContents(self, text_contents):
        self.paras = text_contents.split('\n')
        
    def build(self):
        logging.debug('Building PDF...')
        if len(self.paras) > 0:
            self.fable_doc = fablepage.FableDoc(self._title)
            self._parseFile()
            self._addCover()
            self.fable_doc.addTitle(self._title)
            for chapter in self.chapters:
                self._buildChapter(self.fable_doc, chapter)
        else:
            logging.debug('CRITICAL PDF Error: empty contents.')
            raise
        self.fable_doc.build() 
        
    def save(self, file_h):
        self.fable_doc.save(file_h)
        
    def _parseFile(self):
        """ Divide paragraphs in chapters """
        chapter_paragraphs = []
        chapter_nr = 1
        for paragraph in self.paras:
            if ((paragraph.startswith('Chapter') or (paragraph.startswith('END-OF-FILE')))):
                if (len(chapter_paragraphs) > 0):
                    self._addChapter(chapter_paragraphs)
                    chapter_nr += 1
                    chapter_paragraphs = []
            chapter_paragraphs.append(paragraph)       
        
    def _addCover(self):
        cover_filepath = utils.get_from_resources(self.coverfilename)
        self.fable_doc.addCover(utils.get_google_app_path(cover_filepath))
                
    def _addChapter(self, paragraphs):
        """ Add a chapter to chapters list """
        new_chapter = chapter.FableChapter()
        new_chapter.title = paragraphs[0]
        for i in range(1,len(paragraphs)):
            new_chapter.addParagraph(paragraphs[i])
        self.chapters.append(new_chapter)
            
    def _buildChapter(self, fable, chapter):
        fable.addChapterTitle(chapter.title)
        for paragraph in chapter.paragraphs:
            fable.addParagraphOrImage(paragraph)
        fable.addPageBreak()
                
    def __get_fable(self):
        return self.fable_doc
    
    def __get_pdffile(self):
        return self.pdffilepath
        
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_pdffile, doc="""Get the fable file path.""")
        

    
    