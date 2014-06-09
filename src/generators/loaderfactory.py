""" 
 
 FableGenerator
 
 loaderfactory.py
 
"""

import pdfgenerator.loader as pdf_loader
import epubgenerator.loader as epub_loader
import character

def LoaderFactory(config, use_google = False):
    loader = None
    fable_character = character.GeneratorCharacter(config.name, config.sex, config.birthdate)
    if (config.ebook_format == 'PDF'):
        if (use_google):
            loader = pdf_loader.GoogleLoader(config.fable_id, config.lang, fable_character, config.dedication)
        else:
            loader = pdf_loader.SimpleLoader(config.fable_id, config.lang, fable_character, config.dedication)
    else: # EPUB
        loader = epub_loader.EPubLoader(config.fable_id, config.lang, fable_character, config.dedication)
    return loader


        
    