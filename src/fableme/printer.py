""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 print.py

"""

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.writer import Writer

from google.appengine.ext.webapp.util import login_required

class Print(FablePage):
    """ /print page """ 
    
    def _prepare(self, user, fable_id):
        """ read the template and prepare for pdf creation """
        self.fable = Fabulator(user, fable_id) 
        self.fablewriter = Writer(self.fable.the_fable)
    
    @login_required    
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.the_user, long(fable_id))
        self.template_values['fable_id'] = fable_id
        self.template_values['fable_contents'] = self.fablewriter.get_fable()
        self.template_values['title'] = self.fablewriter.get_title()
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'print.html')
        
class PrintPDF(Print):
    """ /print page """ 
    
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.the_user, long(fable_id))
        nick = self.fable.the_fable.name
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        self._prepare(self.the_user, long(fable_id))
        self.template_values['downloadURL'] = '/serve/%s?nick=%s&lastmod=%s' % ( self.fablewriter.get_pdf(), nick, lastmod )
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'download.html')
        
        