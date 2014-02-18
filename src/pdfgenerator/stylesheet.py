'''
PDFGenerator
stylesheet.py

@author: Alessio Saltarin
'''

from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import fableme.utils as utils

pdfmetrics.registerFont(TTFont('Calibri', utils.GoogleUtils.get_from_resources('calibri.ttf')))
pdfmetrics.registerFont(TTFont('CalibriBold', utils.GoogleUtils.get_from_resources('calibrib.ttf')))
pdfmetrics.registerFont(TTFont('CalibriItalics', utils.GoogleUtils.get_from_resources('calibrii.ttf')))
pdfmetrics.registerFont(TTFont('CalibriBoldItalics', utils.GoogleUtils.get_from_resources('calibriz.ttf')))

# Initialization
_baseFontName = 'Calibri'
_baseFontNameI = 'CalibriItalics'
_baseFontNameB = 'CalibriBold'
_baseFontNameBI = 'CalibriBoldItalics'


def fableMeStyleSheet():
    """Returns the FableMe stylesheet """
    
    stylesheet = StyleSheet1()

    stylesheet.add(ParagraphStyle(name='Normal',
                                  fontName=_baseFontName,
                                  firstLineIndent=5,
                                  fontSize=16,
                                  leading=24,
                                  spaceBefore=4,
                                  spaceAfter=4)
                   )

    stylesheet.add(ParagraphStyle(name='BodyText',
                                  parent=stylesheet['Normal'],
                                  spaceBefore=6)
                   )
    stylesheet.add(ParagraphStyle(name='Italic',
                                  parent=stylesheet['BodyText'],
                                  fontName = _baseFontNameI)
                   )

    stylesheet.add(ParagraphStyle(name='Title',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=26,
                                  leading=24,
                                  alignment=TA_CENTER,
                                  spaceAfter=6),
                   alias='title')

    stylesheet.add(ParagraphStyle(name='Chapter',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameI,
                                  fontSize=18,
                                  leading=18,
                                  spaceBefore=12,
                                  spaceAfter=20,
                                  textColor=darkblue),
                   alias='chapter')

    stylesheet.add(ParagraphStyle(name='Heading3',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameBI,
                                  fontSize=12,
                                  leading=14,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h3')

    stylesheet.add(ParagraphStyle(name='Heading4',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameBI,
                                  fontSize=10,
                                  leading=12,
                                  spaceBefore=10,
                                  spaceAfter=4),
                   alias='h4')

    stylesheet.add(ParagraphStyle(name='Heading5',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=9,
                                  leading=10.8,
                                  spaceBefore=8,
                                  spaceAfter=4),
                   alias='h5')

    stylesheet.add(ParagraphStyle(name='Heading6',
                                  parent=stylesheet['Normal'],
                                  fontName = _baseFontNameB,
                                  fontSize=7,
                                  leading=8.4,
                                  spaceBefore=6,
                                  spaceAfter=2),
                   alias='h6')

    stylesheet.add(ParagraphStyle(name='Bullet',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  spaceBefore=3),
                   alias='bu')

    stylesheet.add(ParagraphStyle(name='Definition',
                                  parent=stylesheet['Normal'],
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  bulletIndent=0,
                                  spaceBefore=6,
                                  bulletFontName=_baseFontNameBI),
                   alias='df')

    stylesheet.add(ParagraphStyle(name='Code',
                                  parent=stylesheet['Normal'],
                                  fontName='Courier',
                                  fontSize=8,
                                  leading=8.8,
                                  firstLineIndent=0,
                                  leftIndent=36))

    return stylesheet
