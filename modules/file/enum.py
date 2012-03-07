

from core.module import Module, ModuleException
from core.parameters import ParametersList, Parameter as P
import os

classname = 'Enum'

class Enum(Module):
    """Enumerate paths on remote filesystem"""
     
    params = ParametersList('Enumerate remote paths specified by wordlist', None,
                P(arg='lpath', help='Path of local wordlist', required=True, pos=0))


    def __init__(self, modhandler, url, password):
        self.list = []
        
        Module.__init__(self, modhandler, url, password)
     
    def set_list(self, list):
        """Cleaned after use"""
        self.list = list
     
    def run_module(self, list_path):
        
        if not self.list and list_path:
            
            try:
                list=open(os.path.expanduser(list_path),'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path)
        else:
            list = self.list[:]
            self.list = []

        self.mprint('[%s] Enumerating %i paths' % (self.name, len(list)))
        
        for path in list:
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'exists'}):
                output += '\texists'
                
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'r'}):
                    output += ', +readable'
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'w'}):
                    output += ', +writable'
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'x'}):
                    output += ', +excutable'
                                         
                self.mprint(output)
                
            
                        
                    
                    
        
        
            