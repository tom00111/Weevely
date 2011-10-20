import os
from module import ModuleException
from config import Config
from modules_info import ModInfos

class ModHandler(dict):
    
    def __init__(self, url = None, password = None, path_modules = 'modules'):
        
        self.url = url
        self.password = password
        
        if not os.path.exists(path_modules):
            raise Exception( "No module directory %s found." % path_modules )
        
        self.path_modules = path_modules

        self.loaded_shells = []    
        self.modules = {}
        
        self.modinfo = ModInfos()
        self.module_info = self.modinfo.module_info
        
        self.conf = Config(self.modinfo.module_info.keys())
        
        
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


                        
                
                
                
                    
                
            
    
                
                