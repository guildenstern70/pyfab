"""
FableGenerator
epubgenerator.fablepage.py

@author: Alessio Saltarin
"""

import os
import sys
import logging
import zipfile
import StringIO

import generators.textformatter as textformatter
import epubheaders

EPUB_SOURCES_DIR = "resources/epubfiles/"
EPUB_OUTPUT_DIR = "../output"
EPUB_MASTER_FILE = "index.html"
EPUB_PROTO_FILE = "index_prototype.html"
EPUB_INDEX_FILE = "content.opf"
PAGE_BREAK = "<div style='page-break-before:always;'></div>"

class EPubFableDoc(textformatter.TextFormatter):
    
    def __init__(self, fabletitle, standalone):
        self._story = ""
        self._index = ""
        self._titlepage = ""
        self._id_counter = 1
        self._language = "en-US"
        self._title = fabletitle
        self._init_epubfiles()
        
    def _init_epubfiles(self):
        self._zipfilelist = [
            EPUB_SOURCES_DIR + 'mimetype',
            EPUB_SOURCES_DIR + 'META-INF/container.xml',
            EPUB_SOURCES_DIR + 'page_styles.css',
            EPUB_SOURCES_DIR + 'stylesheet.css',
            EPUB_SOURCES_DIR + 'toc.ncx',
        ]
        
    def initialize(self, iso_language):
        self._setInitialXHTML(iso_language)
        self._setInitialIndex(iso_language)
        
    def addCover(self, coverImageFile):
        baseFileName = os.path.basename(coverImageFile)
        self._zipfilelist.append(coverImageFile)
        self._index += '   <item href="'
        self._index += baseFileName
        self._index += '" id="cover" media-type="image/jpeg"/>'
        self._titlepage = self._titlepage.replace('********', baseFileName)
    
    def prepareImageFromText(self, imageTextDescription, loader):
        imageFileName = None
        try:
            if imageTextDescription[5] == '[':
                imageFileName = imageTextDescription[6:imageTextDescription.find(']')].split(',')
                imageFilePath = loader.get_images_path_to(imageFileName[0])
                self._zipfilelist.append(imageFilePath)
        except:
            logging.error('Cannot parse image descriptor: ' + imageTextDescription)
            logging.error('Unexpected error: ' + str(sys.exc_info()[1]))
        return imageFileName[0]
    
    def addTitle(self, text, dedication):
        _template = """<p class="fableme1">&#160;</p><p class="fableme4 fablemecenter">FableMe.com</p>
        <div class="booktitle">{title}</div><p class="fableme1">&#160;</p>
        <p class="fableme1">&#160;</p><p class="fableme1">&#160;</p>
        <p class="fableme4 fablemecenter">{dedication}</p>"""
        _template = _template.replace('{title}', text)
        dedicPar = ""
        for dedicLine in dedication.split('***'):
            dedicPar += dedicLine
            dedicPar += "<br/>"
        _template = _template.replace('{dedication}', dedicPar)
        _template += PAGE_BREAK
        self._index = self._index.replace('{title}', text)
        self._story += _template
    
    def addChapterTitle(self, chapter_title):
        _template = """<div class="chaptertitle"><p class="fableme1">&#160;</p><i class="fableme4">{chaptertitle}</i></div>"""
        _template = _template.replace('{chaptertitle}', chapter_title)
        _template += """<p class="fableme1">&#160;</p>"""
        self._story += _template
    
    def addPageBreak(self):
        self._story += PAGE_BREAK
    
    def addParagraphOrImage(self, text, loader):
        if text.startswith('**IMG'):
            self._id_counter += 1
            idname = 'id' + str(self._id_counter)
            imageName = self.prepareImageFromText(text, loader)    
            _template = """<div class="fableimage">
            <img alt="Image" src="{image_src}"/>
            </div>"""
            _template = _template.replace('{image_src}', imageName)
            _index = """<item href="{imagefilename}" id="{imgid}" media-type="image/jpeg"/>"""
            _index = _index.replace('{imagefilename}', imageName)
            _index = _index.replace('{imgid}', idname)
            self._index += _index
        else:
            _template = """<p class="fableme1">{ptext}</p>"""
            _template = _template.replace('{ptext}', text)
        if _template is not None:
            self._story += _template
        else:
            logging.critical('*Warning: image is None!')
                    
    def build(self):
        self._story += """</body></html>"""
        self._index += epubheaders.EPUB_INDEX_FOOTER

    def save(self, epub_fullname):
        epub_absolute = os.path.join(os.getcwd(), epub_fullname)
        logging.debug(' - EPUB SAVE Writing ePub file: %s', epub_absolute)
        if self.zip_files(epub_absolute):
            logging.debug(' - ePub file created successfully.')
        logging.debug(' - Done.')
        
    def save_h(self, epub_file_handler):
        logging.debug(' - EPUB SAVE with handler ePub file:')
        if self.zip_files_h(epub_file_handler):
            logging.debug(' - ePub file created successfully.')
        logging.debug(' - Done.')
        
    def zip_files_h(self, zip_file_h):
        save_succeeded = True        
        try:       
            stream = StringIO.StringIO()
            with zipfile.ZipFile(stream, 'w') as fzip:
                logging.debug('ZIP - Adding mimetype')
                fzip.write(self._zipfilelist[0], arcname='mimetype') # mimetype
                fzip.write(self._zipfilelist[1], arcname='META-INF/container.xml') # META-INF
                for zfile in self._zipfilelist[2:]:
                    fname = os.path.basename(zfile)
                    logging.debug('ZIP - Adding '+zfile)
                    fzip.write(zfile, arcname=fname, compress_type=zipfile.ZIP_DEFLATED)
                fzip.writestr('index.html', self._story.encode('utf-8'))
                fzip.writestr('titlepage.xhtml', self._titlepage.encode('utf-8'))
                fzip.writestr('content.opf', self._index.encode('utf-8'))
            logging.debug('Serializing...')
            zip_file_h.write(stream.getvalue())
            logging.debug('Done serializing.')
        except:
            logging.error('Error saving ePub Zip file with handler')
            logging.error('Unexpected error: ' + str(sys.exc_info()[1]))
            save_succeeded = False
        return save_succeeded
              
    def zip_files(self, zip_file):
        save_succeeded = True
        try:
            if os.path.isfile(zip_file):
                logging.debug(' - Removing existing old '+zip_file)
                os.remove(zip_file)
            with zipfile.ZipFile(zip_file, 'w') as fzip:
                logging.debug('ZIP - Adding mimetype')
                fzip.write(self._zipfilelist[0], arcname='mimetype') # mimetype
                fzip.write(self._zipfilelist[1], arcname='META-INF/container.xml') # META-INF
                for zfile in self._zipfilelist[2:]:
                    fname = os.path.basename(zfile)
                    logging.debug('ZIP - Adding '+zfile)
                    fzip.write(zfile, arcname=fname, compress_type=zipfile.ZIP_DEFLATED)
                fzip.writestr('index.html', self._story.encode('utf-8'))
                fzip.writestr('titlepage.xhtml', self._titlepage.encode('utf-8'))
                fzip.writestr('content.opf', self._index.encode('utf-8'))
        except:
            logging.error('Error saving ePub Zip file')
            logging.error('Unexpected error: ' + str(sys.exc_info()[1]))
            save_succeeded = False
        return save_succeeded
    
    def _setInitialXHTML(self, iso_language):
        xhtmlContents = epubheaders.EPUB_XHTML_HEADER
        self._story = xhtmlContents.replace('{iso_lang}', iso_language)
        self._story = self._story.replace('{title}', self._title)
        self._titlepage = epubheaders.EPUB_XHTML_TITLEPAGE
        
    def _setInitialIndex(self, language):
        self._index = epubheaders.EPUB_INDEX_HEADER
        self._index = self._index.replace('{language}', language)
        
        
            
    
    