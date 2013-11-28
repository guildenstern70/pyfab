""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 booktemplates.py
 
"""


books = (
         {
            'template_id': 0,
            'template_text_file': 'When_I_met_the_Pirates.txt',
            'template_dir': 'When_I_met_the_Pirates',
            'title': 'When I met the Pirates',
            'title_RO': 'xxxxx',
            'title_IT': 'Quando incontrai i pirati',
            'sku': 'SKU #83321',
            'languages': 'English, Italian',
            'issuu_id': '8025851/5449283',
            'cover_image': 'When_I_met_the_Pirates.jpg',
            'bookimg_girl': 'cover_pirates_girl.jpg',
            'bookimg_boy': 'cover_pirates.jpg',
            'sidebar_pic': 'rustic_pirate.jpg',
            'prot_boy': 'prot_pirate_boy.jpg',
            'prot_girl': 'prot_pirate_girl.jpg',
            'sex_recomm': 'MF',
            'age_recomm_min': 4,
            'age_recomm_max': 10,
            'author_img':'dana.jpg',
            'author_name': 'Dana Sandu',
            'author_ill':'Noha',
            'author_desc': '''Dana Sandu is Chief Officer at FableMe, and a recognized writer 
                              of fables and novels for teenagers. She has a beautiful daughter, 
                              Diana, who is the first passionate lover of FableMe.com fables!''',
            'desc_title': 'A great adventure...',
            'desc_desc': '''"When I met the Pirates" is a beautiful pirate story for boys and girls all over the world. 
                            The hero, Peter, joins an interesting crew made of a dog pirate, a cat pirate, 
                            a parrot pirate and a rat pirate. Together they sail the seas and have 
                            a lot of fun...''',
            'desc_short': '''The hero, Peter, joins an interesting crew made of a dog pirate, a cat pirate, 
                            a parrot pirate and a rat pirate. Together they sail the seas and have 
                            a lot of fun....'''
            
            },
             {
                'template_id': 1,
                'template_text_file': 'My_voyage_to_Aragon.txt',
                'template_dir' : 'My_voyage_to_Aragon',
                'title': 'My voyage to Aragon',
                'title_RO': 'xxxxx',
                'title_IT': 'Il mio viaggio ad Aragon',
                'sku': 'SKU #83203',
                'languages': 'English',
                'issuu_id': '8868387/4252762',
                'cover_image': 'My_voyage_to_Aragon.jpg',
                'bookimg_girl': 'cover_voyage.jpg',
                'bookimg_boy': 'cover_voyage_boy.jpg',
                'sex_recomm': 'MF',
                'age_recomm_min': 4,
                'age_recomm_max': 16,
                'sidebar_pic': 'Anna.jpg',
                'prot_boy': 'prot_voyage_boy.jpg',
                'prot_girl': 'prot_voyage_girl.jpg',
                'author_img':'dana.jpg',
                'author_name': 'Dana Sandu',
                'author_ill':'Noha',
                'author_desc': '''Dana Sandu is Chief Officer at FableMe, and a recognized writer 
                                  of fables and novels for teenagers. She has a beautiful daughter, 
                                  Diana, who is the first passionate lover of FableMe.com fables!''',
                'desc_title': 'A dream comes true',
                'desc_desc': """This is the story of little Anna, a beautiful princess who travels 
                                to the land of Aragon and discovers that wisdom (knowledge) and wit
                                (perception and learning) are both needed in life. It is written 
                                with a medieval feel and as a rhyming ode. The story follows 
                                Anna who is riding to school on her pony and becomes distracted 
                                when they meet a fox. She, her pony and the fox begin a journey 
                                through the forest. As the princess progresses through the adventures 
                                she reflects after each one on the moral or learning point.""",
                'desc_short': '''A beautiful princess travels 
                                to the land of Aragon and discovers that wisdom and wit
                                are both needed in life...'''
                
            },
         {
            'template_id': 2,
            'template_text_file': 'The_talisman_of_the_Badia.txt',
            'template_dir' : 'The_talisman_of_the_Badia',
            'title': 'The Amazing story of the Badia Talisman',
            'title_RO': 'xxxxx',
            'title_IT': 'La fantastica storia del talismano della Badia',
            'sku': 'SKU #83232',
            'languages': 'English, Italian',
            'issuu_id': '',
            'cover_image': 'The_talisman_of_the_Badia.jpg',
            'bookimg_girl': 'cover_badia.jpg',
            'bookimg_boy': 'cover_badia.jpg',
            'sex_recomm': 'MF',
            'age_recomm_min': 9,
            'age_recomm_max': 99,
            'sidebar_pic': 'Capture.jpg',
            'prot_boy': 'prot_badia_boy.jpg',
            'prot_girl': 'prot_badia_girl.jpg',
            'author_img':'alessio.jpg',
            'author_name': 'Alessio Saltarin',
            'author_ill':'Noha',
            'author_desc': '''Alessio Saltarin is an italian writer of novels and short-stories.
                              In his spare time he designs and programs videogames.''',
            'desc_title': 'An old tale retold again',
            'desc_desc': """In a green and flat land crossed by a river whose waters flowed 
                            impetuous and full of fish, a young princess is imprisoned in the
                            high tower of a castle. Young Andrew, the so-called God-Of-The-Turks,
                            comes out of the blue to rescue her. A classic fable for every
                            dreamer boy or girl.""",
            'desc_short': '''A young princess is imprisoned in the
                            high tower of a castle. Young Andrew, the so-called God-Of-The-Turks,
                            comes out of the blue to rescue her.'''
        }
    )



class Book(object):
    """ Incapsulates the books dictionary into a class """
    
    def __init__(self, book_id):
        self.dictionary = books[book_id]
        for k, v in self.dictionary.items():
            setattr(self, k, v)
 
    def recommendation(self):
        recomm = "Recommended for "
        age_min = self.dictionary['age_recomm_min']
        age_max = self.dictionary['age_recomm_max']
        sex_recomm = self.dictionary['sex_recomm']
        if (sex_recomm == 'M'):
            recomm += " boys"
        elif (sex_recomm == 'F'):
            recomm += " girls"
        else:
            recomm += " boys and girls"
        recomm += " aged "
        recomm += str(age_min)
        recomm += "-"
        recomm += str(age_max)
        recomm += " years."
        return recomm
    
def get_all_books():
    books_collection = []
    for i in range(0, len(books)):
        books_collection.append(Book(i))
    return books_collection

def get_book_template(book_id):
    """
        # Book 0 -> Peter and the Pirates
        # Book 1 -> Anna goes to Aragon 
        # Book 2 -> The talisman of the Badia  
        
    """ 
    return books[int(book_id)]
        