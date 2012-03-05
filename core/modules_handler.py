import os
from module import ModuleException
from vector import VectorList, Vector 
from helper import Helper


class ModHandler(Helper):
    
    interpreters_priorities = [ 'shell.sh', 'shell.php' ]
    
    
    def __init__(self, url = None, password = None, path_modules = 'modules'):
        
        self.url = url
        self.password = password
        
        if not os.path.exists(path_modules):
            raise Exception( "No module directory %s found." % path_modules )
        
        self.path_modules = path_modules

        self.loaded_shells = []    
        self.modules = {}

        Helper.__init__(self)
        
        
        self.verbosity=3
        
        self.interpreter = None
            
#        self.__load_interpreters()
        
        
    def load(self, module_name, init_module = True, disable_interpreter_probe=False):
        
        if not module_name in self.modules:
            if module_name not in self.module_info.keys():
                raise ModuleException(module_name,   "Module not found in path '%s'." % (self.path_modules) )
            
            mod = __import__('modules.' + module_name, fromlist = ["*"])
            modclass = getattr(mod, mod.classname)
            if not init_module:
                return modclass
            
            self.modules[module_name]=modclass(self, self.url, self.password)
            if module_name.startswith('shell.'):
                self.loaded_shells.append(module_name)
            
        
        return self.modules[module_name]
         
                    
    def set_verbosity(self, v = 3):
        self.verbosity = v        
#                
#    def get_default_interpreter(self):
#        
#        
#        for interp in self.interpreters_priorities:
#            if interp in self.loaded_shells:
#                return interp
#        
                
                
    def load_interpreters(self):
        
        for interpr in self.interpreters_priorities:
            
            try:
                self.load(interpr)
            except ModuleException, e:
                print '[!] [%s] %s' % (e.module, e.error)   
            else:
                self.interpreter = interpr
                return self.interpreter
            
        
        raise ModuleException('[!]', 'No remote backdoor found. Check URL and password.') 
#   
                
                