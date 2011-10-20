'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException
from tempfile import NamedTemporaryFile
from os import remove

classname = 'Read'
    
class Read(Module):
    '''Read file from remote filesystem
    :file.read <remote path> 
    '''
        
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)

          
    def run(self, remote_path):
        
        file = NamedTemporaryFile() 
        file.close()
        
        response = self.modhandler.load('file.download').run(remote_path, file.name, True)
            
        if response:
            remove(file.name)
            return response
            
        raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
