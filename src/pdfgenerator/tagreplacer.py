""" 
 
 PdfGenerator
 
 tagreplacer.py
 
"""

from numtoword.num2word_EN import to_card, to_ord, to_ordnum

INITIAL_TAG_SYMBOL = '{'
FINAL_TAG_SYMBOL = '}'

#Known_tags = ['<i>', '</i>', '<b>', '</b>', '<bi>', '</bi>', '<para>', '</para>', '<br/>']

class Replacer(object):
    '''
    Logic to replace tags to actual word in template
    '''

    def __init__(self, template, character):
        self.fable_template = template
        self.character_sex = character.sex
        self.character_name = character.name
        self.character_age = character.age
        
    def get_replacements(self):
        ''' Return a dictionary: <tag>: replacement word '''
        self.tags = self._extract_tags_from_template()
        print '-- Found %i tags...' % len(self.tags)
        replacements = self._build_dictionary()
        return replacements
        
    def _extract_tags_from_template(self):
        ''' Return a set (unique list) of tags found in a template '''
        intag = False
        tag = ""
        tags_found = set()
        for ch in self.fable_template:
            if (ch == INITIAL_TAG_SYMBOL):
                intag = True
            elif (ch == FINAL_TAG_SYMBOL):
                intag = False
                tags_found.add(tag+FINAL_TAG_SYMBOL)
                tag = ""
            if (intag):
                tag += ch
        return tags_found
    
    def _build_dictionary(self):
        tag_dict = {}
        for tag in self.tags:
            tag_dict[tag] = self._tag_replace(self.character_sex,tag)
        return tag_dict
    
    def _tag_replace(self, sex, tag):
        ''' A tag with underscore <his_her> is turned into 'his' if male, else 'her'
            A tag without underscore is processed turning the key into the value, ie.: <name> => 'Alessio' '''
        to_be_replaced = ''

        underindex = tag.find('_') 
        if underindex > 0:
            if (sex == 'F'): 
                to_be_replaced = tag[1:underindex] 
            else:
                to_be_replaced = tag[underindex+1:-1]
        else:
            to_be_replaced = tag[1:-1]
        to_be_replaced = self._element_translate(to_be_replaced)
            
        return to_be_replaced
    
    def _element_translate(self, elem):
        ''' Elem is a tag containing a word (M,F substitution has been already done).
            If tag contains <name> return the character's name.
            If tag contains <age> returns the character's age (in letters, ie: six)
            If tag contains <ageplus> returns the character's age + 1 (in letters, ie: seven)
            If tag containg <ageord> returns the character's age in ordinal (in letters, ie: sixth)
            If tag contains <ageplusord> returns the character's age in ordinal + 1 (in letters, ie: seventh)
            This procedure analyzes the tag element and it translates it if it matches certain pre-defined
            keys, such as: name '''
        return {
            'name': self.character_name,
            'age': to_card(self.character_age),
            'ageord': to_ord(self.character_age),
            'ageplus': to_card(self.character_age+1),
            'ageplusord': to_ord(self.character_age+1)
            }.get(elem, elem)    # 9 is default if x not found
    
