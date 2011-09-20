'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.http.request import Request

classname = 'Check'
    
class Check(Module):
    '''Check remote files using different techniques
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
        
        self.vector = None
        self.interpreter = None
        
        Module.__init__(self, modhandler, url, password)    
    
    def run(self, remote_path, mode):
        
        payload = None
        
        for i in self.vectors:
            if mode in self.vectors[i]:
                self.interpreter = i
                self.vector = mode
                payload = self.vectors[i][mode] % (remote_path)
                break
                
                
        if payload:
            
            response = self.modhandler.load(self.interpreter).run(payload)
                
            if response == '1':
                return True
            elif (mode == 'md5' and response):
                return response
            else:
                print 'False, or file not found.'
                return False
        
        raise ModuleException(self.name,  "File check failed, use exists|file|dir|md5|r|w|x as option.")
            
            
                