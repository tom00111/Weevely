import os
from module import ModuleException

class ModDict(dict):
    
    def __init__(self, path_modules = 'modules'):
        
        
        if not os.path.exists(path_modules):
            raise Exception( "No module directory %s found." % path_modules )
        
        
        self.path_modules = path_modules
        self.module_info = {}
        self.load_module_list(path_modules)
        
    def load(self, module_name, url, password):
        
        if not module_name in self:
            
            if module_name not in self.module_info.keys():
                raise ModuleException("moduledict",  "Module not found in path %s." % (self.path_modules) )
            
            mod = __import__('modules.' + module_name, fromlist = ["*"])
            modclass = getattr(mod, mod.classname)
            self[module_name]=modclass(self, url, password)


    def load_module_list(self, dir):
        
        for f in os.listdir(dir):
            
            f = dir + os.sep + f
            
            if os.path.isdir(f):
                self.load_module_list(f)
            if os.path.isfile(f) and f.endswith('.py') and not f.endswith('__init__.py'):
                f = f[8:-3].replace('/','.')
                mod = __import__('modules.' + f, fromlist = ["*"])
                modclass = getattr(mod, mod.classname)
                self.module_info[f] = [ modclass.visible, modclass.__doc__ ]

    
                
                