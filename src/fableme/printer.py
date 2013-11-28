""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 print.py

"""

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.pdfhelper import PdfProxy

from google.appengine.ext.webapp.util import login_required

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
    
    def _build(self):
        self.pdfproxy.prepare_pdf()
        
    def _download_url(self, blobkey, nick, moddate):
        return '/serve/%s?nick=%s&lastmod=%s' % ( blobkey, nick, moddate )
    
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.the_user, long(fable_id))
        self._build()
        blobkey = self.pdfproxy.save_pdf()
        nick = self.fable.the_fable.name
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        self.template_values['downloadURL'] = self._download_url(blobkey, nick, lastmod)
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'download.html')
        
        