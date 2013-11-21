'''
PDFGenerator
chapter.py

@author: Alessio Saltarin
'''

class FableChapter():
    
    def __init__(self):
        self._chapter_title = ""
        self._chapter_paragraphs = []
        
    def addParagraph(self, text):
        self._chapter_paragraphs.append(text)
        
    def ___get_title(self):
        return self._chapter_title
    
    def ___set_title(self, title):
        self._chapter_title = title
        
    def ___get_paras(self):
        return self._chapter_paragraphs
        
    title = property(___get_title, ___set_title,
                         doc="""Gets or sets the title.""")
    
    paragraphs = property(___get_paras, doc="""Gets paragraphs.""")