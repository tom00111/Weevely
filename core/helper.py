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


    def helps(self, module):
        
        output = ''
        
        
        for group in self.ordered_groups:
            
            if not module:
                output += '[%s]\n' % group
            
            for modname in self.modules_names_by_group[group]:
                    
                # Considering module name with or without :
                if (module in modname) or (module[1:] in modname) or not module:
                    
                    descr = self.module_info[modname][0]
                    usage = self.module_info[modname][1]
                    help = ''
                    if module:
                       help = '\t%s\n' % self.module_info[modname][2]
                    
                    output += '\t[%s] %s\n\tUsage :%s %s\n\t%s\n' % (modname, descr, modname, usage, help)
             
        if module and not output:
            output += '[!] Error, module \'%s\' not found' % (module) 
        
        return output
            