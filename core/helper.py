import os


class Helper:    


    def __init__(self):
        self.module_info = {}
        self.ordered_module_names = {}
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
                    

    def summaries(self):

        module_dict={}
        output = ''
        
        for mod in self.module_info:
            parts = mod.split('.')
            if parts[0] not in module_dict:
                module_dict[parts[0]] = []
            module_dict[parts[0]].append(':' + mod)
            
        ordered_module_dict = module_dict.keys()
        ordered_module_dict.sort()
            
        for mod in ordered_module_dict:
            output += '  [%s] %s\n' % (mod, ', '.join(module_dict[mod]))
            
        return output


    def helps(self, module):
        
        output = ''
        
        for modname in self.module_info:
            
            # Considering module name with or without :
            if (module in modname) or (module[1:] in modname) or not module:
                
                descr = self.module_info[modname][0]
                usage = self.module_info[modname][1]
                help = ''
                if module:
                   help = '%s\n' % self.module_info[modname][2]
                
                output += '[%s] %s\nUsage :%s %s\n%s\n' % (modname, descr, modname, usage, help)
         
        if module and not output:
            output += '[!] Error, module \'%s\' not found' % (module) 
        
        return output
            