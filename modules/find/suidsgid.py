'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Suidsgid'
    
class Suidsgid(Module):
    '''Find suid|sgid|all file 
    :find.suidsgid suid|sgid|all <path> 
    '''
    
    vectors = {
               "shell.sh" : {
                             'find' : "find %s %s 2>/dev/null"
                }
          }
    
    visible = True
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        


    def run(self, mod, path):
        
        if mod == 'all':
            mod = '-perm -04000 -o -perm -02000'
        elif mod == 'suid':
            mod = '-perm -04000'
        elif mod == 'sgid':
            mod = '-perm -02000'
        else:
            raise ModuleException("find.suidsgid",  "Find suid/sgid failed. Use suid|sgid|all as parameter.")
         
        
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                    
                    payload = self.vectors[interpreter][vector] % (path, mod)
                    print "[find.suidsgid] Finding using method '%s'" % (vector)  
                              
                    if interpreter == 'shell.sh':       
                        response = self.modhandler.load(interpreter).run(payload, False)
    
                    if response:
                        return response
                
                
        raise ModuleException("find.suidsgid",  "Find failed.")
            

        

    
    
    