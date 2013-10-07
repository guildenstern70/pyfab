'''
PDFGenerator
main.py

@author: Alessio Saltarin
'''

import loader

FABLE_FILE = 'My_voyage_to_Aragon.txt'
FABLE_TITLE = 'My voyage to Aragon'

#FABLE_FILE = 'When_I_met_the_Pirates.txt'
#FABLE_TITLE = 'When I met the Pirates'
    
if __name__ == '__main__':
    print 'PDF Generator v.0.1'
    print
    print '-- Generating canvas...'
    fabledoc = loader.FableLoader(filename = FABLE_FILE, title=FABLE_TITLE)
    fabledoc.build()
    print '-- Done.'
    print '-- Saving PDF to ' + fabledoc.fable_file
    print '-- Please wait...'
    try:
        fabledoc.fable.save()
        print '-- PDF successfully saved'
    except IOError:
        print 'ERROR: Cannot write file. In use by another process?'
    print
    print 'All done. Bye.'
    