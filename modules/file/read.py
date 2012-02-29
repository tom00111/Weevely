'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException
from tempfile import NamedTemporaryFile
from core.parameters import ParametersList, Parameter as P
from os import remove
from modules.file.download import Download


classname = 'Read'
    
class Read(Module):

    vectors = Download.vectors
        
    params = ParametersList('Read file from remote filesystem', vectors,
                    P(arg='rpath', help='Choose remote file path', required=True, pos=0)
                    )
    
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)

          
    def run_module(self, remote_path):
        
        file = NamedTemporaryFile() 
        file.close()
        
        # Passing vector to file.download
        self.modhandler.load('file.download').params.set_and_check_parameters({'vector':self.params.get_parameter_value('vector')})
        response = self.modhandler.load('file.download').run_module(remote_path, file.name, True)
        
        if response:
            remove(file.name)
            return response
            
        raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
