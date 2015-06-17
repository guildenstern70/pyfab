""" 
 FableMe.com
 A LittleLite Web Application
 
 version.py

"""

# Version variables
VERSION_MAJOR = 0
VERSION_MINOR = 9
VERSION_BUILD = 9217

# Get version
def version():
    """ FableMe version """
    return str(VERSION_MAJOR)+"."+str(VERSION_MINOR)+"."+str(VERSION_BUILD)
