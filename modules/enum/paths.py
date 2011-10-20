

from core.module import Module, ModuleException

classname = 'Paths'

class Paths(Module):
    """Enumerate file paths. Load list list from file 
    :enum.paths <path_list.txt> 
    """
     
    def run(self, list_path, list = []):
        
        if not list and list_path:
            try:
                list=open(list_path,'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list_path)


        print 'Enumerating %i paths' % (len(list))
        
        for path in list:
            
            output = path + '' + '\t'*(3-((len(path)+1)/8))
            
            if self.modhandler.load('file.check').run(path, 'exists', quiet=True):
                output += '\texists'
                
                if self.modhandler.load('file.check').run(path, 'r', quiet=True):
                    output += ', +readable '
                if self.modhandler.load('file.check').run(path, 'w', quiet=True):
                    output += ', +writable '
                if self.modhandler.load('file.check').run(path, 'x', quiet=True):
                    output += ', +excutable '
                                     
                print output
                        
                    
                    
        
        
            