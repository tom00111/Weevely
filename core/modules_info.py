import os


class ModInfos:    


    def __init__(self):
        self.module_info = {}
        self.load_module_infos()

    def load_module_infos(self, path_modules = 'modules', recursion = True):
        
        for f in os.listdir(path_modules):
            
            f = path_modules + os.sep + f
            
            if os.path.isdir(f) and recursion:
                self.load_module_infos(f, False)
            if os.path.isfile(f) and f.endswith('.py') and not f.endswith('__init__.py'):
                f = f[8:-3].replace('/','.')
                mod = __import__('modules.' + f, fromlist = ["*"])
                modclass = getattr(mod, mod.classname)
                self.module_info[f] = [ modclass.visible, modclass.__doc__ ]
                
        return self.module_info
                    

    def print_module_summary(self):
        
        
        module_dict={}
        
        print ''
        for mod in self.module_info:
            parts = mod.split('.')
            if parts[0] not in module_dict:
                module_dict[parts[0]] = []
            module_dict[parts[0]].append(':' + mod)
            
        ordered_module_dict = module_dict.keys()
        ordered_module_dict.sort()
            
        for mod in ordered_module_dict:
            print '[%s] %s' % (mod, ', '.join(module_dict[mod]))


    def print_module_infos(self):
        
        module_dict={}
        
        print ''
        for mod in self.module_info:
            parts = mod.split('.')
            if parts[0] not in module_dict:
                module_dict[parts[0]] = {}
            module_dict[parts[0]][parts[1]] = self.module_info[mod][1]
            
        ordered_module_dict = module_dict.keys()
        ordered_module_dict.sort()
        
        for pkg in ordered_module_dict:
            
            oldpkg=''
            
            for mod in module_dict[pkg]:
                
                if pkg != oldpkg:
                    output = '[%s] [%s]' % ( pkg,  mod )
                    oldpkg = pkg
                else:
                    output = '%s[%s]' % ( ' '*(len(pkg)+3), mod )
                
                print output,
                
                if module_dict[pkg][mod] and len(module_dict[pkg][mod])>1:
                    lines = module_dict[pkg][mod].split('\n')
                    usageline = lines[-1].strip()
                    titleline = lines[0].strip()
                    
                    print titleline
                    for line in lines[1:-1]:
                        print ' '*(len(pkg)+2), line.strip()
                    print usageline,
                else:
                    print ''
                    
                print ''