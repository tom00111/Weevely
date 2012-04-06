

from core.module import Module, ModuleException
from core.parameters import ParametersList, Parameter as P
import os

classname = 'Enum'

class Enum(Module):
    """Enumerate paths on remote filesystem"""
     
    params = ParametersList('Enumerate remote paths specified by wordlist', None,
                P(arg='lpath', help='Path of local wordlist', required=True, pos=0))


    def __init__(self, modhandler, url, password):
        self.pathdict = {}
        
        Module.__init__(self, modhandler, url, password)
     
    def set_list(self, list):
        """Cleaned after use"""
     
        for p in list:
            self.pathdict[p] = [0,0,0,0]
     
    def get_list(self):
        pathdict = self.pathdict.copy()
        self.pathdict = {}
        return pathdict
     
    def run_module(self, list_path):
        
        if not self.pathdict and list_path:
            
            try:
                list=open(os.path.expanduser(list_path),'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path)
        else:
            list = self.pathdict.keys()


        self.mprint('[%s] Enumerating %i paths' % (self.name, len(list)))
        
        
        for path in list:
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'exists'}):
                output += '\texists'
                
                self.pathdict[path][0] = 1
                
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'r'}):
                    self.pathdict[path][1] = 1
                    output += ', +readable'
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'w'}):
                    self.pathdict[path][2] = 1
                    output += ', +writable'
                if self.modhandler.load('file.check').run({'rpath' : path, 'mode' : 'x'}):
                    self.pathdict[path][3] = 1
                    output += ', +excutable'
                                         
                self.mprint(output)
                
            
                        
                    
                    
        
        
            