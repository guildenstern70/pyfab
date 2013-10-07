'''
PDFGenerator
loader.py

@author: Alessio Saltarin
'''

import sys
import os
import fablepage
import chapter

OUTPUT_DIR = "../../output/"
RESOURCES_DIR = "../../resources/"
        
def output_path(name):
    return os.path.join(OUTPUT_DIR, name)

def resource_path(name):
    return os.path.join(RESOURCES_DIR, name)

class FableLoader():
    
    def __init__(self, filename, title):
        self._filename = filename
        self._title = title
        self.pdffilepath = output_path(os.path.splitext(filename)[0] + '.pdf')
        self.coverfilename = os.path.splitext(filename)[0] + '.png' 
        self.fable = fablepage.FableDoc(self.pdffilepath, title)
        self.chapters = []
        
    def build(self):
        if (self._readFile()):
            self._parseFile()
            self._addCover()
            self.fable.addTitle(self._title)
            for chapter in self.chapters:
                self._buildChapter(self.fable, chapter)
        
    def _readFile(self):
        """ Transfer file contents into paragraphs list """
        fileReadOk = True
        print '  Reading file ' + self._filename
        try:
            fileobj = open(resource_path(self._filename), "r")
            filecontents = fileobj.read()
            fileobj.close()
            self.paras = filecontents.split('\n')
            print '  The file has ' + str(len(self.paras)) + ' paragraphs.'
        except IOError:
            print '*** Critical error opening ', self._filename
            print '*** ', sys.exc_info()[0]
            fileReadOk = False
        return fileReadOk
        
    def _parseFile(self):
        """ Divide paragraphs in chapters """
        if (len(self.paras) == 0):
            print 'No paragraphs found.'
            return
        print '  Parsing file...'
        chapter_paragraphs = []
        chapter_nr = 1
        for paragraph in self.paras:
            if ((paragraph.startswith('Chapter') or (paragraph.startswith('<para')))):
                if (len(chapter_paragraphs) > 0):
                    self._addChapter(chapter_paragraphs)
                    chapter_nr += 1
                    chapter_paragraphs = []
            chapter_paragraphs.append(paragraph)       
        print '  Done.'
        
    def _addCover(self):
        print '  Adding cover'
        self.fable.addCover(resource_path(self.coverfilename))
                
    def _addChapter(self, paragraphs):
        """ Add a chapter to chapters list """
        new_chapter = chapter.FableChapter()
        new_chapter.title = paragraphs[0]
        for i in range(1,len(paragraphs)):
            new_chapter.addParagraph(paragraphs[i])
        self.chapters.append(new_chapter)
            
    def _buildChapter(self, fable, chapter):
        print '  Adding chapter > ' + chapter.title
        fable.addChapterTitle(chapter.title)
        for paragraph in chapter.paragraphs:
            fable.addParagraphOrImage(paragraph)
        fable.addPageBreak()
                
    def __get_fable(self):
        return self.fable
    
    def __get_pdffile(self):
        return self.pdffilepath
        
    fable = property(__get_fable, doc="""Get the fable document.""")
    fable_file = property(__get_pdffile, doc="""Get the fable file path.""")
        

    
    