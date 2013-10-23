""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 booktemplates.py
 
"""

def get_book_template(book_id):
    """
        # Book 0 -> Peter and the Pirates
        # Book 1 -> Anna goes to Aragon 
        # Book 2 -> The talisman of the Badia  
        
    """
            
    if (book_id == '0'):
        book_template = {
            'title': 'When I met the Pirates',
            'sku': 'SKU #83321',
            'bookimg': 'cover_pirates.jpg',
            'sidebar_pic': 'rustic_pirate.jpg',
            'author_img':'dana.jpg',
            'author_name': 'Dana Sandu',
            'author_desc': '''Dana Sandu is Chief Officer at FableMe, and a recognized writer 
                              of fables and novels for teenagers. She has a beautiful daughter, 
                              Diana, who is the first passionate lover of FableMe.com fables!''',
            'desc_title': 'A great adventure...',
            'desc_desc': '''This is a beautiful pirate story for boys and girls all over the world. 
                            The hero, Peter, joins an interesting crew made of a dog pirate, a cat pirate, 
                            a parrot pirate and a rat pirate. Together they sail the sees and have 
                            a lot of fun.''',
            
            }
    elif (book_id == '1'):
        book_template = {
            'title': 'My voyage to Aragon',
            'sku': 'SKU #83203',
            'bookimg': 'cover_voyage.jpg',
            'sidebar_pic': 'Anna.jpg',
            'author_img':'dana.jpg',
            'author_name': 'Dana Sandu',
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
            
        }
    elif (book_id == '2'):
        
        book_template = {
            'title': 'The amazing story of the Badia talisman',
            'sku': 'SKU #83232',
            'bookimg': 'cover_badia.jpg',
            'sidebar_pic': 'Capture.jpg',
            'author_img':'alessio.jpg',
            'author_name': 'Alessio Saltarin',
            'author_desc': '''Alessio Saltarin is an italian writer of novels and short-stories.
                              In his spare time he designs and programs videogames.''',
            'desc_title': 'An old tale retold again',
            'desc_desc': """In a green and flat land crossed by a river whose waters flowed 
                            impetuous and full of fish, a young princess is imprisoned in the
                            high tower of a castle. Young Andrew, the so-called God-Of-The-Turks,
                            comes out of the blue to rescue her. A classic fable for every
                            dreamer boy or girl."""
        }
        
    return book_template
        