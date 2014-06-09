""" 
 FableMe.com
 A LittleLite Web Application
 
 print.py

"""

import urllib

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.generatorhelper import GeneratorProxy

from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class Print(FablePage):
    """ /print page """ 
    
    def _prepare(self, user, fable_id):
        """ read the template """
        self.fable = Fabulator(user, fable_id) 
        self.ebookproxy = GeneratorProxy('unknown', self.fable.the_fable)
        self.fable_contents = self.ebookproxy.load_template()
    
    @login_required    
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.the_user, long(fable_id))
        self.template_values['fable_id'] = fable_id
        self.template_values['fable_contents'] = self.fable_contents
        self.template_values['title'] = self.fable.the_fable.localized_title
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'print.html')
        
class PrinteBook(Print):
    """ /print/book page """ 
    
    def _prepare(self, user, fable_id, fable_format):
        """ read the template and prepare for pdf creation """
        self.fable = Fabulator(user, fable_id) 
        self.ebookproxy = GeneratorProxy(fable_format, self.fable.the_fable)
        self.fable_contents = self.ebookproxy.load_template()
    
    def _build(self, fable_id, fable_format):
        self._prepare(self.the_user, long(fable_id), fable_format)
        self.ebookproxy.prepare_ebook()
        
    def _download_url(self):
        blobkey = self.ebookproxy.save_ebook()
        nick = self.fable.the_fable.name
        titlebrief = self.fable.the_fable.template['title_brief']
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        userid = self.user_db.nickname
        lang = self.fable.the_fable.language
        fmt = self.fable_format
        return '/serve/%s?brief=%s&nick=%s&lastmod=%s&userid=%s&title=%s&lang=%s&fmt=%s' % ( blobkey, titlebrief, nick, lastmod, userid, titlebrief, lang, fmt )
    
    @login_required
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self.fable_format = self.request.get('fmt') 
        self._build(fable_id, self.fable_format)
        self.template_values['downloadURL'] = self._download_url()
        self.template_values['bookFormat'] = self.fable_format
        self.render()
        
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'download.html')
        
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Download the ebook """
    
    @login_required
    def get(self, resource):
        """ http get handler """
        briefname = self.request.get('brief')
        nickname = self.request.get('nick')
        lastmod = self.request.get('lastmod')
        userid = self.request.get('userid')
        lang = self.request.get('lang')
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        ext = '.pdf'
        if (self.request.get('fmt')=='EPUB'):
            ext = '.epub'
        # deve contenere id utente, nome (corto) fiaba, nome bimbo, lingua fiaba, data generazione fiaba.
        ebook_file_name = briefname + '_' + userid + '_' + nickname + '_' + lastmod + '_' + lang + ext
        self.send_blob(blob_info, save_as=ebook_file_name)

        
        