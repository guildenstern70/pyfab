""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 tagreplacer.py
 
"""

class Replacer(object):
    '''
    Logic to replace tags to actual word in template
    '''

    def __init__(self, template, sex, name):
        self.fable_template = template
        self.character_sex = sex
        self.character_name = name
        
    def get_replacements(self):
        self.tags = self._extract_tags_from_template()
        return self._build_dictionary()
        
    def _extract_tags_from_template(self):
        ''' Return a set (unique list) of tags found in a template '''
        intag = False
        tag = ""
        tags_found = set()
        for ch in self.fable_template:
            if (ch == '<'):
                intag = True
            elif (ch == '>'):
                intag = False
                tags_found.add(tag+'>')
                tag = ""
            if (intag):
                tag += ch
        return tags_found
    
    def _build_dictionary(self):
        ''' Return a dictionary: <tag>: replacement word '''
        tag_dict = {}
        for tag in self.tags:
            tag_dict[tag] = self._tag_replace(self.character_sex,tag)
        return tag_dict
    
    def _tag_replace(self, sex, tag):
        ''' A tag with underscore <his_her> is turned into 'his' if male, else 'her'
            A tag without underscore is processed turning the key into the value, ie.: <name> => 'Alessio' '''
        replaced_word = ''
        underindex = tag.find('_')
        if underindex > 0:
            if (sex == 'F'): 
                replaced_word = tag[1:underindex] 
            else:
                replaced_word = tag[underindex+1:-1]
        else:
            if (tag == '<name>'):
                replaced_word = self.character_name
        return replaced_word

        