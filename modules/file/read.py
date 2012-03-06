'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException
from tempfile import NamedTemporaryFile
from core.parameters import ParametersList, Parameter as P
from os import remove, path
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
        
        self.modhandler.set_verbosity(2)
        self.modhandler.load('file.download').run({'rpath' : remote_path, 'lpath' : file.name})
        self.modhandler.set_verbosity()
        
        response = self.modhandler.load('file.download').get_last_read_file()
        if response and path.exists(file.name):
            remove(file.name)
            return response
            
        raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
