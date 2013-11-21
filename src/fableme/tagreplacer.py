""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 tagreplacer.py
 
"""

known_tags = ['<i>', '</i>', '<b>', 
              '</b>', '<bi>', '</bi>', '<para>', '</para>', '<br/>']

class Replacer(object):
    '''
    Logic to replace tags to actual word in template
    '''

    def __init__(self, template, sex, name):
        self.fable_template = template
        self.character_sex = sex
        self.character_name = name
        
    def get_replacements(self):
        ''' Return a dictionary: <tag>: replacement word '''
        self.tags = self._extract_tags_from_template()
        replacements = self._build_dictionary()
        return replacements
        
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
        tag_dict = {}
        for tag in self.tags:
            tag_dict[tag] = self._tag_replace(self.character_sex,tag)
        return tag_dict
    
    def _tag_replace(self, sex, tag):
        ''' A tag with underscore <his_her> is turned into 'his' if male, else 'her'
            A tag without underscore is processed turning the key into the value, ie.: <name> => 'Alessio' '''
        to_be_replaced = ''
        replace_tag = True
        
        for knowntag in known_tags:
            if tag.startswith(knowntag[:-1]):
                to_be_replaced = tag
                replace_tag = False
                break
                
        if replace_tag:
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
        ''' Tag Element: if tag is <his_her>, there are two elements inside: his and her.
            A tag <name> contains the element name.
            This procedure analyzes the tag element and it translates it if it matches certain pre-defined
            keys, such as: name '''
        ret_val = elem
        if (elem == 'name'):
            ret_val = self.character_name
        return ret_val
    
    
    
        

        