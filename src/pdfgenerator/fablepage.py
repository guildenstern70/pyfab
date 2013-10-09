'''
PDFGenerator
fablepage.py

@author: Alessio Saltarin
'''

import stylesheet
import logging
import fableme.utils as utils
import fabletemplate

from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import cm

_W, _H = (21*cm, 29.7*cm) # This is the A4 size
_WF, _HF = (17*cm, 25*cm) # This is the size of a full size flowable
LEFT_MARGIN = 1.5*cm

def firstPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.restoreState()
    
def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(_W/2, 820, 'FableMe - %s' % doc.title)
    canvas.drawCentredString(_W/2, 40, '- %d -' % doc.page)
    canvas.restoreState()

class FableDoc(object):
    
    def __init__(self, fabletitle):
        self._doc = fabletemplate.FableMeDocTemplate(None, 
                                      title=fabletitle,
                                      pagesize=A4, 
                                      topMargin=2*cm,
                                      bottomMargin=2*cm,
                                      leftMargin=2*cm,
                                      rightMargin=2*cm)
        self._story = []
        self._styles = stylesheet.fableMeStyleSheet()
        
    def addCover(self, coverImageFile):
        image = Image(coverImageFile, _WF, _HF)
        image.vAlign = 'TOP'
        self._story.append(image)
        self._story.append(PageBreak())
        
    def getImageFromText(self, imageTextDescription):
        """ The image text descriptor is a sort of tag
            with the following syntax:
            **IMG[filename,image_width,image_height]
            The tag must begin with **IMG[
            and followed the relative path to the image,
            the image width in centimeters
            the image height in centimeters
        """ 
        image = None
        try:
            if (imageTextDescription[5] == '['):
                imageFileDesc = imageTextDescription[6:imageTextDescription.find(']')].split(',')
                imageFileName = utils.get_from_resources(imageFileDesc[0])
                imageFileWidth = float(imageFileDesc[1])
                imageFileHeight = float(imageFileDesc[2])
                image = Image(imageFileName, imageFileWidth*cm, imageFileHeight*cm)
        except:
            logging.critical('Cannot parse image descriptor: ' + imageTextDescription)
        return image
        
    def addTitle(self, text):
        p = Paragraph(text, self._styles["Title"])
        self._story.append(Spacer(1, 1.2*cm))
        self._story.append(p)
        self._story.append(Spacer(1, 2.2*cm))
        
    def addChapterTitle(self, chapter_title):
        p = Paragraph(chapter_title, self._styles['Chapter'])
        self._story.append(Spacer(1, 1.2*cm))
        self._story.append(p)
        
    def addPageBreak(self):
        self._story.append(PageBreak())
        
    def addParagraphOrImage(self, text):
        if (text.startswith('**IMG')):
            flowable = self.getImageFromText(text)
        else:
            flowable = Paragraph(text, self._styles["Normal"])
        if (flowable != None):
            self._story.append(flowable)
            self._story.append(Spacer(1, 0.2*cm))
        else:
            logging.critical('*Warning: image is None!')
        
    def save(self, filename):
        self._doc.build(self._story, file_h=filename, onFirstPage=firstPages, onLaterPages=laterPages)
        
        
        
    
    