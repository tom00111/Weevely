import os
from module import ModuleException

class ModHandler(dict):
    
    def __init__(self, url = None, password = None, path_modules = 'modules'):
        
        self.url = url
        self.password = password
        
        if not os.path.exists(path_modules):
            raise Exception( "No module directory %s found." % path_modules )
        
        self.path_modules = path_modules

        self.loaded_shells = []        
        self.module_info = {}
        self.modules = {}
        
        self.load_module_infos(path_modules)
        
        
    def load(self, module_name):
        
        if not module_name in self.modules:
            if module_name not in self.module_info.keys():
                raise ModuleException("!",  "Module not found in path %s." % (self.path_modules) )
            
            mod = __import__('modules.' + module_name, fromlist = ["*"])
            modclass = getattr(mod, mod.classname)
            self.modules[module_name]=modclass(self, self.url, self.password)
            
            if module_name.startswith('shell.'):
                self.loaded_shells.append(module_name)
            
        return self.modules[module_name]
    

    def load_module_infos(self, dir):
        
        for f in os.listdir(dir):
            
            f = dir + os.sep + f
            
            if os.path.isdir(f):
                self.load_module_infos(f)
            if os.path.isfile(f) and f.endswith('.py') and not f.endswith('__init__.py'):
                f = f[8:-3].replace('/','.')
                mod = __import__('modules.' + f, fromlist = ["*"])
                modclass = getattr(mod, mod.classname)
                self.module_info[f] = [ modclass.visible, modclass.__doc__ ]
                    

    def print_module_infos(self):
        
        print ''
        oldpart=''
        for mod in self.module_info:
            parts = mod.split('.')
            
            if parts[0] != oldpart:
                output = '\n[%s] [%s]' % ( parts[0],  mod )
                oldpart = parts[0]
            else:
                output = '\n%s[%s]' % ( ' '*(len(parts[0])+2), mod )
            
            print output,
            if len(self.module_info[mod][1])>1:
                lines = self.module_info[mod][1].split('\n')
                usageline = lines[-1].strip()
                titleline = lines[0].strip()
                
                print titleline
                for line in lines[1:-1]:
                    print ' '*(len(parts[0])+2), line.strip()
                print usageline
                    
                
                
                
                    
                
            
    
                
                