'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Suidsgid'
    
class Suidsgid(Module):
    '''Find superuser files
    :find.suidsgid suid | sgid | any <path> 
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
        
        if mod == 'any':
            mod = '-perm -04000 -o -perm -02000'
        elif mod == 'suid':
            mod = '-perm -04000'
        elif mod == 'sgid':
            mod = '-perm -02000'
        else:
            raise ModuleException(self.name,  "Find suid/sgid failed. Use suid|sgid|any as parameter.")
         
         
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, mod, path)
        
        
        
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                    response = self.__execute_payload(interpreter, vector, mod, path)
                    if response:
                        return response
                    

        raise ModuleException(self.name,  "No file found")

                    
    def __execute_payload(self, interpreter, vector, mod, path):
        
        payload = self.vectors[interpreter][vector] % (path, mod)
        print "[find.suidsgid] Finding using method '%s'" % (vector)  
                  
        if interpreter == 'shell.sh':       
            response = self.modhandler.load(interpreter).run(payload, False)

        if response:
            return response
            
                
            

        

    
    
    