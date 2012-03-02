

from core.module import Module, ModuleException
from core.parameters import ParametersList, Parameter as P

classname = 'Paths'

class Paths(Module):
    """Enumerate paths on remote filesystem"""
     
    params = ParametersList('Enumerate remote paths specified by wordlist', None,
                P(arg='lpath', help='Path of local wordlist', required=True, pos=0))

     
    def run_module(self, list_path, list = []):
        
        if not list and list_path:
            try:
                list=open(list_path,'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path)

        self.mprint('[%s] Enumerating %i paths' % (self.name, len(list)))
        
        for path in list:
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run_module(path, 'exists'):
                output += '\texists'
                
                if self.modhandler.load('file.check').run_module(path, 'r'):
                    output += ', +readable'
                if self.modhandler.load('file.check').run_module(path, 'w'):
                    output += ', +writable'
                if self.modhandler.load('file.check').run_module(path, 'x'):
                    output += ', +excutable'
                                         
                self.mprint(output)
                
            
                        
                    
                    
        
        
            