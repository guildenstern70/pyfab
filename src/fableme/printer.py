""" 
 FableMe.com
 A LittleLite Web Application
 
 print.py

"""

import logging
import datetime
import fableme.db.schema as schema
from fableme.fabulator import Fabulator
from fableme.abstract import FablePage
from fableme.generatorhelper import GeneratorProxy
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from fableme.webuser import WebUser


class Print(FablePage):
    """ /print page """ 
    
    def __init__(self, request, response):
        FablePage.__init__(self, request, response, 'print.html')
    
    def _prepare(self, user_email, fable_id):
        """ read the template """
        self.fable = Fabulator(user_email, fable_id) 
        db_fable = Fabulator.get_fable(user_email, fable_id)
        self.ebookproxy = GeneratorProxy('unknown', self.fable.the_fable)
        self.fable_contents = '\n' + db_fable.localized_title.upper() + '\n\n'
        self.fable_contents += db_fable.dedication + '\n'
        self.fable_contents += db_fable.sender + '\n\n'
        self.fable_contents += self.ebookproxy.load_template()
       
    def get(self):
        """ http get handler """
        fable_id = self.request.get('id') 
        self._prepare(self.logged.email, int(fable_id))
        self.template_values['fable_id'] = fable_id
        self.template_values['fable_contents'] = self.fable_contents
        self.template_values['title'] = self.fable.the_fable.localized_title
        self.render()

        
class PrinteBook:
    """
        Print book procedure
        Valid values for fable_format: EPUB, PDF, EBOOK
        When fable_format == EBOOK, every format is generated 
    """ 
    
    def __init__(self, user_email):
        logging.debug('Init Print eBook: user='+user_email)
        self.user_mail = user_email
        self.user_db = schema.DbFableUser.get_from_email(user_email)
    
    def _prepare(self, fable_id, fable_format):
        """ read the template and prepare for pdf creation """
        self.fable = Fabulator(self.user_mail, fable_id) 
        self.ebookproxy = GeneratorProxy(fable_format, self.fable.the_fable)
        self.fable_contents = self.ebookproxy.load_template()
        
    def _build_specific_format(self,  fable_id, fable_format):
        """ Build file, save it and return download link """
        self._prepare(int(fable_id), fable_format)
        self.ebookproxy.prepare_ebook()
        return self._download_url(fable_format)
    
    def _build(self, fable_id, fable_format):
        """ Returns a dictionary containing download links 
            for every format, ie: {'PDF': 'http://www.ddshkdsj.com/833890', 'EPUB': 'http://www.ddshkdsj.com/833891'} """
        download_links = {}
        if fable_format == "EBOOK":
            # PDF
            download_links['PDF'] = self._build_specific_format(fable_id, 'PDF')
            # EPUB
            download_links['EPUB'] = self._build_specific_format(fable_id, 'EPUB')
        else:   
            download_links[fable_format] = self._build_specific_format(fable_id, fable_format)
        return download_links
        
    def _download_url(self, fable_format):
        username = WebUser.nick_from_email(self.user_db.email)
        titlebrief = self.fable.the_fable.template['title_brief']
        lastmod = self.fable.the_fable.modified.strftime("%d%m%y%H%M%S")
        lang = self.fable.the_fable.language
        ext = '.' + fable_format.lower()
        ebook_file_name = titlebrief + '_' + username + '_' + lastmod + '_' + lang + ext
        blobkey = self.ebookproxy.save_ebook(ebook_file_name)
        return '/serve/%s?brief=%s&lastmod=%s&bmail=%s&title=%s&lang=%s&fmt=%s' % \
               (blobkey, titlebrief, lastmod, username, titlebrief, lang, fable_format)
      
    def printbook(self, fable_id, fable_format):
        logging.info('Initiating process print ebook id='+fable_id)
        downlinks = self._build(fable_id, fable_format)
        # Update DB fable
        dbfable = schema.DbFable.get_fable(self.user_mail, int(fable_id))
        dbfable.bought = True
        link_pdf = downlinks.get('PDF')
        link_epub = downlinks.get('EPUB')   
        if link_pdf is not None:
            dbfable.downlink_pdf = link_pdf
        if link_epub is not None:
            dbfable.downlink_epub = link_epub
        dbfable.purchased = datetime.datetime.now()
        dbfable.put()
        logging.info('Ended process pring ebook id='+fable_id)
        dbuser = schema.DbFableUser.get_from_email(self.user_mail)
        logging.info('Sending email advice to '+dbuser.email)
        self.sendmail(dbuser, downlinks)
        
    def sendmail(self, dbuser, ebook_links):     
        receiver = 'FableMe user'
        to_field = dbuser.email
        body_field = """
Dear [name],

The eBook you recently purchased from FableMe.com is ready.  You can now visit
http://www.fableme.com/ and sign in using your Google Account to
download it. To do so, navigate to your Account page, under the tab 'My Purchased eBooks'.

You can also directly download it, by clicking the link below:

http://fableomatic.appspot.com[link]

Sincerely,
Your FableMe Team
        """
        
        html_field = """
        
<div>
<p>Dear [name],</p>

<p>The eBook you recently purchased from FableMe.com is ready.  You can now visit
<a href="http://www.fableme.com/">FableMe.com</a> and sign in using your Google Account to
download it. To do so, navigate to your Account page, under the tab 'My Purchased eBooks'.</p>

<p>You can also directly download it, by clicking the link below.</p>

<p>
<a href="http://fableomatic.appspot.com[link]">Download your eBook</a>
</p>

<p>
Sincerely,<br/>
<i>Your FableMe Team</i>
</p>
</div>
        
        """
        
        link_pdf = ebook_links.get('PDF')
        link_epub = ebook_links.get('EPUB')   
        if link_pdf is not None:
            ebook_link = link_pdf
        if link_epub is not None:
            ebook_link = link_epub     
        body_field = body_field.replace('[name]', receiver)
        body_field = body_field.replace('[link]', ebook_link)
        html_field = html_field.replace('[name]', receiver)
        html_field = html_field.replace('[link]', ebook_link)
        mail.send_mail(sender="FableMe.com Support <support@fableomatic.appspotmail.com>",
                       to=to_field,
                       subject="Your FableMe eBook is ready!",
                       body=body_field,
                       html=html_field)


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """ Download the ebook """
    
    def get(self, resource):
        """ http get handler """
        briefname = self.request.get('brief')
        briefmail = self.request.get('bmail')
        lastmod = self.request.get('lastmod')
        lang = self.request.get('lang')
        ext = '.pdf'
        if self.request.get('fmt') == 'EPUB':
            ext = '.epub'
        # deve contenere id utente, nome (corto) fiaba, nome bimbo, lingua fiaba, data generazione fiaba.
        ebook_file_name = briefname + '_' + briefmail + '_' + lastmod + '_' + lang + ext
        self.send_blob(resource, save_as=ebook_file_name)
