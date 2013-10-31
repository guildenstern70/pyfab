""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 booktemplates.py
 
"""

books = (
         {
            'id': 0,
            'title': 'When I met the Pirates',
            'sku': 'SKU #83321',
            'languages': 'English, Italian',
            'issuu_id': '8025851/5449283',
            'bookimg_girl': 'cover_pirates_girl.jpg',
            'bookimg_boy': 'cover_pirates.jpg',
            'sidebar_pic': 'rustic_pirate.jpg',
            'age_recomm': 'For boys and girls aged 4-10 years',
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
                'id': 1,
                'title': 'My voyage to Aragon',
                'sku': 'SKU #83203',
                'languages': 'English',
                'issuu_id': '8868387/4252762',
                'bookimg_girl': 'cover_voyage.jpg',
                'bookimg_boy': 'cover_voyage_boy.jpg',
                'age_recomm': 'For boys and girls aged 4-7 years',
                'sidebar_pic': 'Anna.jpg',
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
            'id': 2,
            'title': 'The Amazing story of the Badia Talisman',
            'sku': 'SKU #83232',
            'languages': 'English, Italian',
            'bookimg_girl': 'cover_badia.jpg',
            'bookimg_boy': 'cover_badia.jpg',
            'age_recomm': 'For boys and girls aged 9-99 years',
            'sidebar_pic': 'Capture.jpg',
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

def get_book_template(book_id):
    """
        # Book 0 -> Peter and the Pirates
        # Book 1 -> Anna goes to Aragon 
        # Book 2 -> The talisman of the Badia  
        
    """ 
    return books[int(book_id)]
        