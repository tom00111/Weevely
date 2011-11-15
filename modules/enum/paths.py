

from core.module import Module, ModuleException

classname = 'Paths'

class Paths(Module):
    """Enumerate paths on remote filesystem
    :enum.paths <path_list.txt> 
    """
     
    def run(self, list_path, list = []):
        
        if not list and list_path:
            try:
                list=open(list_path,'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path)

        self.mprint('[%s] Enumerating %i paths' % (self.name, len(list)))
        
        for path in list:
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run(path, 'exists'):
                output += '\texists'
                
                if self.modhandler.load('file.check').run(path, 'r'):
                    output += ', +readable'
                if self.modhandler.load('file.check').run(path, 'w'):
                    output += ', +writable'
                if self.modhandler.load('file.check').run(path, 'x'):
                    output += ', +excutable'
                                         
                self.mprint(output)
                
            
                        
                    
                    
        
        
            