from abc import abstractmethod

'''
FableGenerator
generators.textformatter.py

@author: Alessio Saltarin
'''


class TextFormatter(object):
    """
    
        A 'TextFormatter' object transforms text with tags in
        a specific format, ie: PDF, HTML, ePub.
        It converts text elements such as chapters, images, titles
        in corresponding specific technology elements.
        
    """  
    def __init__(self, fabletitle, standalone):
        self._story = []
    
    @abstractmethod
    def addCover(self, coverImageFile):
        return NotImplemented
    
    @abstractmethod
    def getImageFromText(self, imageTextDescription, loader):
        return NotImplemented
    
    @abstractmethod
    def addTitle(self, text):
        return NotImplemented
    
    @abstractmethod
    def addChapterTitle(self, chapter_title):
        return NotImplemented
    
    @abstractmethod
    def addPageBreak(self):
        return NotImplemented
    
    @abstractmethod
    def addParagraphOrImage(self, text, loader):
        return NotImplemented
    
    @abstractmethod
    def build(self):
        return NotImplemented
    
    @abstractmethod
    def save(self):
        pass
    