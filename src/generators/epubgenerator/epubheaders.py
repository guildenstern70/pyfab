'''
FableGenerator
epubgenerator.epubheaders.py

@author: Alessio Saltarin
'''

EPUB_XHTML_TITLEPAGE = """<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Cover</title>
        <style type="text/css" title="override_css">
            @page {padding: 0pt; margin:0pt}
            body { text-align: center; padding:0pt; margin: 0pt; }
        </style>
    </head>
    <body>
        <div>
        <svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 450 684" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
            <image height="684" width="450" xlink:href="********"></image>
        </svg>
        </div>
    </body>
</html>"""

EPUB_XHTML_HEADER = """<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="{iso_lang}" xml:lang="{iso_lang}">
<head>
    <title>{title}</title>
    <meta name="generator" content="FableGenerator"/>
    <meta name="author" content="FableMe.com"/>
    <meta name="keywords" content=""/>
    <meta name="date" content="2013-11-26T16:22:35+00:00"/>
    <meta name="subject" content="A fable"/>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link href="stylesheet.css" rel="stylesheet" type="text/css"/>
    <link href="page_styles.css" rel="stylesheet" type="text/css"/>
</head>
<body class="fableme">"""
      
EPUB_INDEX_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">

  <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
            xmlns:opf="http://www.idpf.org/2007/opf" 
            xmlns:dcterms="http://purl.org/dc/terms/" 
            xmlns:dc="http://purl.org/dc/elements/1.1/">

    <dc:creator>FableMe.com</dc:creator>
    <dc:identifier id="uuid_id" opf:scheme="uuid">f67bfcbc-977e-4ccc-8606-6f613c90c827</dc:identifier>
    <dc:date>0101-01-01T00:00:00+00:00</dc:date>
    <dc:title>{title}</dc:title>
    <dc:subject>(unspecified)</dc:subject>
    <dc:rights>(C) FableMe.com</dc:rights>
    <dc:language>{language}</dc:language>
   
  </metadata>

  <manifest>
     <item href="index.html" id="id1" media-type="application/xhtml+xml"/>
     <item href="page_styles.css" id="page_css" media-type="text/css"/>
     <item href="stylesheet.css" id="css" media-type="text/css"/>
     <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>
     <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
"""

EPUB_INDEX_FOOTER = """</manifest>
  <spine toc="ncx">
    <itemref idref="titlepage"/>
    <itemref idref="id1"/>
  </spine>
  <guide>
    <reference href="titlepage.xhtml" title="Cover" type="cover"/>
  </guide>
</package>
"""