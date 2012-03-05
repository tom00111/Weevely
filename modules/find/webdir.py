'''
Created on 28/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P
from random import choice
from string import letters
from core.http.request import Request
from urlparse import urlparse

classname = 'Webdir'
    
class Webdir(Module):
    '''Find first writable directory and corresponding URL
    :find.webdir auto | <start dir>
    '''
    
    vectors = VectorList([
       V('shell.php', 'fwrite', "fwrite(fopen('%s','w'),'1');"),
       V('shell.php', "file_put_contents" , "file_put_contents('%s', '1');"),
       V('shell.sh', "echo" , "echo '1' > %s"),
    ])
    

    params = ParametersList('Find a writable directory and corresponding URL', vectors,
                    P(arg='rpath', help='Remote starting path', default='auto', pos=0))
    
    
    def __init__( self, modhandler , url, password):

        self.dir = None
        self.url = None
        
        self.probe_filename = ''.join(choice(letters) for i in xrange(4)) + '.html'

        Module.__init__(self, modhandler, url, password)
        



    def __prepare_payload( self, vector, parameters ):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        
    

    def __execute_payload(self, vector, parameters):
        
        dir_path = parameters[0] 
        file_path = parameters[1] 
        file_url = parameters[2] 
        dir_url = parameters[3]
        
        payload = self.__prepare_payload(vector, [ file_path ])
        
        self.modhandler.load(vector.interpreter).run({0 : payload})

        if self.modhandler.load('file.check').run({'rpath' : file_path, 'mode' : 'exists'}):
            
                
            file_content = Request(file_url).read()
            
            if( file_content == '1'):
                self.dir = dir_path
                self.url = dir_url
                
            
            if self.modhandler.load('shell.php').run( { 0 : "unlink('%s') && print('1');" % file_path }) != '1':
                print "[!] [find.webdir] Error cleaning test file %s" % (file_path)
                
            if self.dir and self.url:
                print "[find.webdir] Writable web dir found with method '%s': %s -> %s" % (vector.name, self.dir, self.url)
                return True
                
            
        return False    
                
                        


    def run_module(self, start_dir):
        if self.url and self.dir:
            self.mprint("[%s] Writable web dir: %s -> %s" % (self.name, self.dir, self.url))
            return
            
        if start_dir == 'auto':
            try:
                root_find_dir = self.modhandler.load('system.info').run({ 0 : 'basedir' })
            except ModuleException, e:
                self.mprint('[!] [' + e.module + '] ' + e.error)
                root_find_dir = None
                
        else:
            root_find_dir = start_dir
        
        if root_find_dir:
            
            if not root_find_dir[-1]=='/': root_find_dir += '/'
            
            http_root = '%s://%s/' % (urlparse(self.url).scheme, urlparse(self.url).netloc) 
            
            try:
                writable_dirs_string = self.modhandler.load('find.perms').run({'qty' :  'any','type' : 'd', 'perm' : 'w', 'rpath' : root_find_dir })
                writable_dirs = [ d for d in writable_dirs_string.split('\n') if d]
            except ModuleException as e:
                self.mprint('[!] [' + e.module + '] ' + e.error)
                writable_dirs = []
                
               
            for dir_path in writable_dirs:
            
            
                if not dir_path[-1]=='/': dir_path += '/'
                file_path = dir_path + self.probe_filename
    
                file_url = http_root + file_path.replace(root_find_dir,'')
                dir_url = http_root + dir_path.replace(root_find_dir,'')
            
            
                vectors = self._get_default_vector2()
                if not vectors:
                    vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
                
                for vector in vectors:
                    
                    response = self.__execute_payload(vector, [dir_path, file_path, file_url, dir_url])
                    if response != None:
                        self.params.set_and_check_parameters({'vector' : vector.name})
                        return True
                    
                 
        if not (self.url and self.dir):
            raise ModuleException(self.name,  "Writable web directory not found")