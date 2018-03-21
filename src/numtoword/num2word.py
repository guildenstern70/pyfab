from __future__ import division 

import num2word_EN
import num2word_FR
import num2word_IT
import num2word_RO


class Num2Word(object):
    
    def __init__(self, language='EN'):
        """ Constructor """
        self._lang = language
    
    def create(self):
        if self._lang == 'EN':
            numtoword = num2word_EN.Num2Word_EN()
        elif self._lang == 'IT':
            numtoword = num2word_IT.Num2Word_IT()
        elif self._lang == 'RO':
            numtoword = num2word_RO.Num2Word_RO()
        elif self._lang == 'FR':
            numtoword = num2word_FR.Num2Word_FR()
        else:
            raise Exception("Unsupported language in Num2Word. Currently supported: EN, RO, IT, FR")
        return numtoword


if __name__ == '__main__':
    
    n2w = Num2Word('IT').create()
    
    to_card = n2w.to_cardinal
    to_ord = n2w.to_ordinal
    to_ordnum = n2w.to_ordinal_num
    to_year = n2w.to_year
    
    print('Num2Word v2.0 ')
    print('26 => ' + to_card(26))
    print('45th => ' + to_ord(45))
    print('72 => ' + to_ordnum(72))
    print('1972 => ' + to_year(1972))
