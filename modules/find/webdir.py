'''
Created on 28/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from random import choice
from string import letters
from core.http.request import Request
from urlparse import urlparse

classname = 'Webdir'
    
class Webdir(Module):
    '''Find writable directory in web root with corresponding URL (help file downloads)
    :find.webdir
    '''
    
    vectors = { 'shell.php' : { "fwrite()"       : "fwrite(fopen('%s','w'),'1');",
                           "file_put_contents"             : "file_put_contents('%s', '1');"
                            },
            'shell.sh' : {
                            "echo" : "echo '1' > %s"
                            }
           }
    
    def __init__( self, modhandler , url, password):

        self.dir = None
        self.url = None
        
        self.probe_filename = ''.join(choice(letters) for i in xrange(4)) + '.txt'

        Module.__init__(self, modhandler, url, password)
        

    def __execute_payload(self, interpreter, vector, dir_path, file_path, file_url, dir_url):
        
        payload = self.vectors[interpreter][vector] % file_path
        self.modhandler.load(interpreter).run(payload)

        if self.modhandler.load('shell.php').run("file_exists('%s') && print('1');" % file_path) == '1':
                
            if(Request(file_url).read() == '1'):
                print "[find.webdir] Writable web dir: %s -> %s" % (dir_path, dir_url)
                self.dir = dir_path
                self.url = dir_url
                return
            
            if self.modhandler.load('shell.php').run("unlink('%s') && print('1');" % file_path) != '1':
                print "[!] [find.webdir] Error cleaning test file %s" % (file_path)
                        


    
    def _probe(self):
        
        if self.url and self.dir:
            return
            
        document_root = self.modhandler.load('system.info').run('document_root')
        if not document_root[-1]=='/': document_root += '/'
        
        http_root = '%s://%s/' % (urlparse(self.url).scheme, urlparse(self.url).netloc) 
        
#        print '[find.webdir] Implying that %s URL points to %s, searching for writable web directory' % (http_root, document_root)
        
        writable_dirs = self.modhandler.load('find.perms').run('all', 'dir', 'w', document_root).split('\n')
        
        for dir_path in writable_dirs:
        
            if not dir_path[-1]=='/': dir_path += '/'
            file_path = dir_path + self.probe_filename

            file_url = http_root + file_path.replace(document_root,'')
            dir_url = http_root + dir_path.replace(document_root,'')
        
        
            interpreter, vector = self._get_default_vector()
            if interpreter and vector:
                return self.__execute_payload(interpreter, vector, dir_path, file_path, file_url, dir_url)
        
                
            for interpreter in self.vectors:
                for vector in self.vectors[interpreter]:
                    if interpreter in self.modhandler.loaded_shells:
                        return self.__execute_payload(interpreter, vector, dir_path, file_path, file_url, dir_url)
                        
        
                 
        if not (self.url and self.dir):
            raise ModuleException(self.name,  "Writable web directory corresponding not found")