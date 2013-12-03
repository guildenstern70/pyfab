""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 print.py

"""

import urllib

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.pdfhelper import PdfProxy

from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class Print(FablePage):
    """ /print page """ 
    
    def _prepare(self, user, fable_id):
        """ read the template and prepare for pdf creation """
        self.fable = Fabulator(user, fable_id) 
        self.pdfproxy = PdfProxy(self.fable.the_fable)
        self.fable_contents = self.pdfproxy.load_template()
    
    @login_required    
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.the_user, long(fable_id))
        self.template_values['fable_id'] = fable_id
        self.template_values['fable_contents'] = self.fable_contents
        self.template_values['title'] = self.fable.the_fable.title
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'print.html')
        
class PrintPDF(Print):
    """ /print page """ 
    
    def _build(self, fable_id):
        self._prepare(self.the_user, long(fable_id))
        self.pdfproxy.prepare_pdf()
        
    def _download_url(self):
        blobkey = self.pdfproxy.save_pdf()
        nick = self.fable.the_fable.name
        titlebrief = self.fable.the_fable.template['title_brief']
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        userid = self.user_db.nickname
        lang = 'EN'
        return '/serve/%s?nick=%s&lastmod=%s&userid=%s&title=%s&lang=%s' % ( blobkey, nick, lastmod, userid, titlebrief, lang )
    
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._build(fable_id)
        self.template_values['downloadURL'] = self._download_url()
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'download.html')
        
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Download the PDF """
    
    @login_required
    def get(self, resource):
        """ http get handler """
        nickname = self.request.get('nick')
        lastmod = self.request.get('lastmod')
        userid = self.request.get('userid')
        lang = self.request.get('lang')
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        # deve contenere id utente, nome (corto) fiaba, nome bimbo, lingua fiaba, data generazione fiaba.
        pdf_file_name = 'Fable_' + userid + '_' + nickname + '_' + lastmod + '_' + lang + '.pdf'
        self.send_blob(blob_info, save_as=pdf_file_name)

        
        