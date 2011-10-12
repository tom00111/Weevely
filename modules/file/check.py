'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException

classname = 'Check'
    
class Check(Module):
    '''Check remote files presence, type, md5 and permissions
    :file.check <remote path> exists|file|dir|md5|r|w|x
    '''
    
    
    vectors = { 'shell.php' : { 
                           "exists"             : "$f='%s'; (file_exists($f) || is_readable($f) || is_writable($f) || is_file($f) || is_dir($f)) && print(1);",
                           "dir"            : "is_dir('%s') && print(1);",
                           "md5"            : "print(md5_file('%s'));",
                           "r"            : "is_readable('%s') && print(1);",
                           "w"            : "is_writable('%s') && print(1);",
                           "x"            : "is_executable('%s') && print(1);",
                           "file"            : "is_file('%s') && print(1);"
                            }
           }
    
    def __init__(self, modhandler, url, password):

        
        Module.__init__(self, modhandler, url, password)    
    
    def __execute_payload(self, interpreter, vector, remote_path, mode, quiet):
        
        payload = self.vectors[interpreter][vector] % (remote_path)
        response = self.modhandler.load(interpreter).run(payload)
            
        if response == '1':
            return True
        elif (mode == 'md5' and response):
            return response
        else:
            if mode != 'exists':
                if not self.run(remote_path, 'exists', quiet):
                    if not quiet:
                        print 'File not exists.'
            if not quiet:
                print 'False'
                
        return False
        
    
    def run(self, remote_path, mode, quiet = False):
        
        mode_found = False
                
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, remote_path, mode, quiet)
        else:
            for i in self.vectors:
                if mode in self.vectors[i]:
                    mode_found = True
                    response = self.__execute_payload(i, mode, remote_path, mode, quiet)
                    return response
                    
        if not mode_found:
            raise ModuleException(self.name,  "Error, use exists|file|dir|md5|r|w|x as option.")
            
                