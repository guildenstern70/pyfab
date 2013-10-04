""" 
 FABLE-O-MATIC
 A LittleLite Web Application
 
 print.py

"""
import os

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.writer import Writer

from google.appengine.ext.webapp.util import login_required

class Print(FablePage):
    """ /print page """ 
    
    def _prepare(self, user, fable_id):
        """ read the template and prepare for pdf creation """
        fable = Fabulator(user, fable_id) 
        fable_sex = fable.the_fable.sex
        fable_title = fable.the_fable.template
        fable_name = fable.the_fable.name
        if fable_title == 'Peter and the pirates':
            filepath = os.path.join(os.path.split(__file__)[0], '../resources/Peter.txt')
        else:
            filepath = os.path.join(os.path.split(__file__)[0], '../resources/Anna.txt')
        fablefile = open(filepath, 'r')
        filecontents = fablefile.read()
        fablefile.close()
        self.fablewriter = Writer(filecontents, fable_title, fable_sex, fable_name)
    
    @login_required    
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') # the fable to edit (-1: new fable)
        self._prepare(self.the_user, long(fable_id))
        self.template_values['fable_contents'] = self.fablewriter.get_fable(),
        self.template_values['title'] = self.fablewriter.get_title()
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'print.html')
        
class PrintPDF(Print):
    """ /print page """ 
    
    @login_required
    def get(self):
        """ http get handler """
        self._prepare(self.the_user)
        self.template_values['downloadURL'] = '/serve/%s' % self.fablewriter.get_pdf()
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'download.html')
        
        