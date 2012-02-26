import os
from module import ModuleException
from vector import VectorList, Vector 
from config import Config
from modules_info import ModInfos
from helper import Helper


class ModHandler(Helper):
    
    vectors = VectorList([
        Vector('shell.sh', 'system_shell', ""),
        Vector('shell.php', 'php_shell', "")
        ])
    
    
    def __init__(self, url = None, password = None, path_modules = 'modules'):
        
        self.url = url
        self.password = password
        
        if not os.path.exists(path_modules):
            raise Exception( "No module directory %s found." % path_modules )
        
        self.path_modules = path_modules

        self.loaded_shells = []    
        self.modules = {}

        Helper.__init__(self)
        
        self.modinfo = ModInfos()
        self.module_info = self.modinfo.module_info
        
        self.conf = Config(self.modinfo.module_info.keys())
        
        self.verbosity=3
        
        self.interpreter = None
        
        self.__load_interpreters()
        
        
    def load(self, module_name):
        
        if not module_name in self.modules:
            if module_name not in self.modinfo.module_info.keys():
                raise ModuleException("!",  "Module not found in path %s." % (self.path_modules) )
            
            mod = __import__('modules.' + module_name, fromlist = ["*"])
            modclass = getattr(mod, mod.classname)
            self.modules[module_name]=modclass(self, self.url, self.password)
            if module_name.startswith('shell.'):
                self.loaded_shells.append(module_name)
            
        
        return self.modules[module_name]
                    
    def set_verbosity(self, v = 3):
        self.verbosity = v        
                
                
    def __load_interpreters(self):
        
        for vector in self.vectors:
            
            try:
                self.load(vector.interpreter)
            except ModuleException, e:
                print '[!] [%s] %s' % (e.module, e.error)   
            else:
                self.interpreter = vector.interpreter
                break
   
                
    
            
    
                
                