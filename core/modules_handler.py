import os
from module import ModuleException
from config import Config

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
        
        self.conf = Config(self.module_info.keys())
        
        
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
                    

    def print_module_summary(self):
        
        i = 0
        for mod in self.module_info:
            if i == 5: 
                i = 0
                print ''
            else: i+=1
            print '[ :' +  mod + ' ]',

    def print_module_infos(self):
        
        module_dict={}
        
        print ''
        for mod in self.module_info:
            parts = mod.split('.')
            if parts[0] not in module_dict:
                module_dict[parts[0]] = {}
            module_dict[parts[0]][parts[1]] = self.module_info[mod][1]
            
        
        for pkg in module_dict:
            
            oldpkg=''
            
            for mod in module_dict[pkg]:
                
                if pkg != oldpkg:
                    output = '\n[%s] [%s]' % ( pkg,  mod )
                    oldpkg = pkg
                else:
                    output = '\n%s[%s]' % ( ' '*(len(pkg)+3), mod )
                
                print output,
                
                if len(module_dict[pkg][mod])>1:
                    lines = module_dict[pkg][mod].split('\n')
                    usageline = lines[-1].strip()
                    titleline = lines[0].strip()
                    
                    print titleline
                    for line in lines[1:-1]:
                        print ' '*(len(pkg)+2), line.strip()
                    print usageline,
                        
                
                
                
                    
                
            
    
                
                