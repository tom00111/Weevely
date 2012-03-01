import os


class Helper:    


    def __init__(self):
        self.module_info = {}
        self.modules_names_by_group={}
        self.ordered_groups = []
        
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

                parts = f.split('.')
                if parts[0] not in self.modules_names_by_group:
                    self.modules_names_by_group[parts[0]] = []
                self.modules_names_by_group[parts[0]].append(f)

            
        self.ordered_groups = self.modules_names_by_group.keys()
        self.ordered_groups.sort()                

    def summaries(self):

        output = ''
        
        for group in self.ordered_groups:
            output += '  [%s] %s\n' % (group, ', '.join(self.modules_names_by_group[group]))
            
        return output


    def help_completion(self, module, only_name = False):
        
        matches = []
        
        for group in self.ordered_groups:
            
            for modname in self.modules_names_by_group[group]:
                    
                if(modname == module):
                    return [ modname ]
                    
                # Considering module name with or without :
                elif (modname.startswith(module[1:])) or not module:
                    
                    usage = ''
                    if not only_name:
                        usage = self.module_info[modname][1]
                    matches.append(':%s %s' % (modname, usage))
        
        return matches
                    

    def helps(self, module):
        
        output = ''
        
        for group in self.ordered_groups:
            
            if not module:
                output += '[%s]' % group
            
            for modname in self.modules_names_by_group[group]:
                    
                # Considering module name with or without :
                if (modname.startswith(module)) or (modname.startswith(module[1:])) or not module:
                    
                    descr = self.module_info[modname][0]
                    usage = self.module_info[modname][1]
                    help = ''
                    if module:
                       help = self.load(modname).params.help()
                    
                    output += '\n    [%s] %s\n    Usage :%s %s\n    %s\n' % (modname, descr, modname, usage, help)
             
        if module and not output:
            output += '[!] Error, module \'%s\' not found' % (module) 
        
        return output 
            