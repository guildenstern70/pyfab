""" 
 FableMe.com
 A LittleLite Web Application
 
 character.py

"""

import time
import datetime
import sys

class Character(object):
    """ Attributes of the fable main character """
    
    @classmethod
    def from_fable_db(cls, dbfable):
        return cls(dbfable.name, dbfable.sex, dbfable.birthdate)
    
    @classmethod
    def calculate_age(cls, born):
        today = datetime.date.today()
        try: 
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year
        
    def to_nice_string(self):
        boygirl = 'boy'
        if self.sex == 'F':
            boygirl = 'girl'
        return 'the ' + boygirl + ' ' + self.name + ', ' + str(self.age) + ' years old.' 
    
    def __repr__(self, *args, **kwargs):
        return "[" + self.name + ", " + self.sex + ", Age = " + str(self.age) + "]"

    def __init__(self, cname, csex, cbirthdate):
        self.sex = csex
        self.name = cname
        self.birthdate = cbirthdate
        self.age = self.calculate_age(cbirthdate)
 
        
class PdfGeneratorCharacter(Character):
          
    def get_age(self):
        age = -1
        try:
            birth_date = time.strptime(self.birthdate, "%d-%b-%y")
            birth_datetime = datetime.date.fromtimestamp(time.mktime(birth_date))
            age = self.calculate_age(birth_datetime)
        except:
            print sys.exc_info()
            print
        return age
    
    def __init__(self, cname, csex, cbirthdate):
        self.sex = csex
        self.name = cname
        self.birthdate = cbirthdate
        self.age = self.get_age()

        