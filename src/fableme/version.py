""" 
 FableMe.com
 A LittleLite Web Application
 
 version.py

"""

# Global variables
VERSION_MAJOR = 0
VERSION_MINOR = 9
VERSION_BUILD = 8777

# Global methods
def version():
    """ FableMe version """
    return str(VERSION_MAJOR)+"."+str(VERSION_MINOR)+"."+str(VERSION_BUILD)
