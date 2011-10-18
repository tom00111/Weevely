

from core.module import Module, ModuleException

classname = 'Enumerate'

class Enumerate(Module):
    """Enumerate files. Load list list from file or specify path list
    :file.enumerate  load:<path_list.txt> | <path1>,...,<pathN> 
    """
     
    def run(self, list_path, list = []):
        
        if not list and list_path:
            if list_path.startswith('load:'):
                try:
                    list=open(list_path[5:],'r').read().splitlines()
                except:
                    raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path[5:])
            else:
                list = list_path.split(',')
            
        for path in list:
            
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run(path, 'exists', quiet=True):
                output += 'exists'
                
                if self.modhandler.load('file.check').run(path, 'r', quiet=True):
                    output += ', +readable '
                if self.modhandler.load('file.check').run(path, 'w', quiet=True):
                    output += ', +writable '
                if self.modhandler.load('file.check').run(path, 'x', quiet=True):
                    output += ', +excutable '
                                     
            print output
                        
                    
                    
        
        
            