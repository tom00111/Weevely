'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random

classname = 'Console'
 

    
class Console(Module):
    '''Start SQL console
    :sql.console mysql|postgres <host> <user> <pass>
    '''

    def __init__( self, modhandler , url, password):
            

        Module.__init__(self, modhandler, url, password)
        
        

    def run( self, mode, host, user, pwd):

        self.mprint('[%s] Console have no state, commands like \'USE database\' are ineffective. Press Ctrl-C to quit.\n' % (self.name))

        prompt        = "%s@%s SQL> " % (user, host)
        
        self.modhandler.set_verbosity(2)

        try:
            while True:
                
                cmd       = raw_input( prompt )
                cmd       = cmd.strip()
                
                if cmd:
                    response = self.modhandler.load('sql.query').run(mode, host, user, pwd, cmd)
                    if response:
                        print response
                    else:
                        self.mprint('[%s] No data returned' % self.name, 2)
        
        except KeyboardInterrupt:
            self.modhandler.set_verbosity()
            raise
            
    
    