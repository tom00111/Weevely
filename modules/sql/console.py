'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random

classname = 'Summary'
 

    
class Summary(Module):
    '''Get SQL database summary
    :sql.query mysql|postgres <host> <user> <pass> 
    '''
    

    def __init__( self, modhandler , url, password):
            

        Module.__init__(self, modhandler, url, password)
        
        

    def run( self, mode, host, user, pwd):

        while True:
            
            prompt        = "%s@%s SQL>" % (user, host)

            cmd       = raw_input( prompt )
            cmd       = cmd.strip()
            
            if cmd:
                response = self.modhandler.load('sql.query').run(mode, host, user, pwd, payload)
                
    
    
    