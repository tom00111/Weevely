import os


class ModInfos:    


    def __init__(self):
        self.module_info = {}
        self.load_infos()


    def load_infos(self, name=None, dir = 'modules', recursion = True):
        
        for f in os.listdir(dir):
            
            f = dir + os.sep + f
            
            if os.path.isdir(f) and recursion:
                self.load_infos(None, f, False)
            if os.path.isfile(f) and f.endswith('.py') and not f.endswith('__init__.py'):
                f = f[8:-3].replace('/','.')
                mod = __import__('modules.' + f, fromlist = ["*"])
                modclass = getattr(mod, mod.classname)
                self.module_info[f] = [ modclass.params.module_description, modclass.params.summary(), modclass.params.help() ]
                    

    def summary(self):

        module_dict={}
        
        for mod in self.module_info:
            parts = mod.split('.')
            if parts[0] not in module_dict:
                module_dict[parts[0]] = []
            module_dict[parts[0]].append(':' + mod)
            
        ordered_module_dict = module_dict.keys()
        ordered_module_dict.sort()
            
        for mod in ordered_module_dict:
            print '[%s] %s' % (mod, ', '.join(module_dict[mod]))
            
        print ''


    def help(self, module):
        
        for modname in self.module_info:
            
            if (module in modname) or not module:
                
                descr = self.module_info[modname][0]
                usage = self.module_info[modname][1]
                help = ''
                if module:
                   help = '%s' % self.module_info[modname][2]
                
                print '\n[%s] %s\nUsage :%s %s\n%s' % (modname, descr, modname, usage, help)
                

            