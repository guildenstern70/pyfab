""" 
 FableMe.com
 A LittleLite Web Application
 
 print.py

"""

import logging
import urllib
import datetime

import fableme.db.schema as schema

from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.generatorhelper import GeneratorProxy
from google.appengine.api import mail

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
        
class PrinteBook():
    """ /print/book page """ 
    
    def _prepare(self, user, fable_id, fable_format):
        """ read the template and prepare for pdf creation """
        self.fable = Fabulator(user, fable_id) 
        self.ebookproxy = GeneratorProxy(fable_format, self.fable.the_fable)
        self.fable_contents = self.ebookproxy.load_template()
    
    def _build(self, fable_id, fable_format, user):
        self._prepare(user, long(fable_id), fable_format)
        self.ebookproxy.prepare_ebook()
        
    def _download_url(self, fable_format):
        blobkey = self.ebookproxy.save_ebook()
        nick = self.fable.the_fable.name
        titlebrief = self.fable.the_fable.template['title_brief']
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        userid = self.user_db.nickname
        lang = self.fable.the_fable.language
        return '/serve/%s?brief=%s&nick=%s&lastmod=%s&userid=%s&title=%s&lang=%s&fmt=%s' % ( blobkey, titlebrief, nick, lastmod, userid, titlebrief, lang, fable_format )
      
    def printBook(self, fable_id, fable_format):
        logging.info('Initiating process print ebook id='+fable_id)
        self._build(fable_id, fable_format, self.user)
        # Update DB fable
        dbfable = schema.DbFable.get_fable(self.user, long(fable_id))
        dbfable.bought = True
        link_url = self._download_url(fable_format)
        dbfable.downlink = link_url
        dbfable.purchased = datetime.datetime.now()
        dbfable.put()
        logging.info('Ended process pring ebook id='+fable_id)
        dbuser = schema.DbFableUser.get_from_user(self.user)
        logging.info('Sending email advice to '+dbuser.email)
        self.sendmail(dbuser, link_url)
        
    def sendmail(self, dbuser, ebook_link):     
        receiver = 'user'
        if (dbuser.name):
            receiver = dbuser.name.title()
        elif (dbuser.nickname):
            receiver = dbuser.nickname.title()
        to_field = receiver + ' <' + dbuser.email + '>'
        body_field = """
Dear [name],

The eBook you recently purchased from FableMe.com is ready.  You can now visit
http://www.fableme.com/ and sign in using your Google Account to
download it. To do so, navigate to your Account page, under the tab 'Purchased eBooks'.

You can also directly download it, by clicking the link below:

http://www.fableme.com/[link]

Sincerely,
Your FableMe Team
        """
        
        body_field = body_field.replace('[name]', receiver)
        body_field = body_field.replace('[link]', ebook_link)
        mail.send_mail(sender="FableMe.com Support <support@fableomatic.appspotmail.com>",
                      to=to_field,
                      subject="Your FableMe eBook is ready!",
                      body=body_field)
        
    def __init__(self, user):
        self.user = user
        self.user_db = schema.DbFableUser.get_from_user(user)
    
        
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

        
        