'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random
from core.parameters import ParametersList, Parameter as P

classname = 'Console'
 

    
class Console(Module):
    '''Start SQL console'''
    
    params = ParametersList('Start SQL console', [],
            P(arg='dbms', help='Database', choices=['mysql', 'postgres'], required=True, pos=0),
            P(arg='user', help='SQL user', required=True, pos=1),
            P(arg='pwd', help='SQL password', required=True, pos=2),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=3)
            )

    def run_module( self, mode, user, pwd, host):

        self.mprint('[%s] No saved state, commands like \'USE database\' are ineffective. Press Ctrl-C to quit.\n' % (self.name))

        prompt        = "%s@%s SQL> " % (user, host)
        
        self.modhandler.set_verbosity(2)

        try:
            while True:
                
                cmd       = raw_input( prompt )
                cmd       = cmd.strip()
                
                if cmd:
                    response = self.modhandler.load('sql.query').run({'dbms' : mode, 'user' : user, 'pwd': pwd, 'query' : cmd, 'host' : host})
                    
                    if response:
                        print response
                    else:
                        self.mprint('[%s] No data returned' % self.name)
        
        except KeyboardInterrupt:
            self.modhandler.set_verbosity()
            raise
            
    
    