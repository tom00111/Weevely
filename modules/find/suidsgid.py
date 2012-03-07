'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

classname = 'Suidsgid'
    
class Suidsgid(Module):
    '''Find files with superuser flags'''
    
    vectors = VectorList([
       V('shell.sh', "find" , "find %s %s 2>/dev/null")
    ])
    
    params = ParametersList('Find files with suid and sgid flags', vectors,
                    P(arg='type', help='Suid, sgid or both', choices=['suid','sgid', 'any'], default='any', pos=0), 
                    P(arg='rpath', help='Remote starting path', default='.', pos=1)
                    )
    
    
    visible = True
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        
        
        
    def run_module(self, type, path):
            
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            
            response = self.__execute_payload(vector, [type, path])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
        
        raise ModuleException(self.name,  "Files not found")

    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters)
    
        try:    
            response = self.modhandler.load(vector.interpreter).run({0 : payload})
        except ModuleException:
            response = None
        else:
            return response

    def __prepare_payload(self, vector, parameters):
        
        mod = parameters[0]
        path = parameters[1]
                
        if vector.interpreter == 'shell.sh':
                
            if mod == 'any':
                mod = '-perm -04000 -o -perm -02000'
            elif mod == 'suid':
                mod = '-perm -04000'
            elif mod == 'sgid':
                mod = '-perm -02000'
             
        return vector.payloads[0] % (path, mod) 
                    
