'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P
import re

classname = 'Ifaces'
    
class Ifaces(Module):

    params = ParametersList('Print network interfaces and corresponding IP/MASK', [])
    
    
    def __find_ifconfig_path(self):
        
        ifconfig_paths = [ x + 'ifconfig' for x in ['/sbin/', '/bin/', '/usr/bin/', '/usr/sbin/', '/usr/local/bin', '/usr/local/sbin'] ]
        
        self.modhandler.load('file.enum').set_list(ifconfig_paths)
        self.modhandler.set_verbosity(6)
        self.modhandler.load('file.enum').run({ 'lpath' : 'fake' })
        self.modhandler.set_verbosity()
        
        ifconfig_dict_paths = self.modhandler.load('file.enum').get_list()    
        for p in ifconfig_dict_paths:
            if ifconfig_dict_paths[p][0]:
                return p
            
    
    def run_module(self):
        
        
        ifconfig = self.__find_ifconfig_path()

        try:
            response = self.modhandler.load('shell.sh').run({ 0 : ifconfig})
        except ModuleException:
            response = None
        
        if response:
            ifaces = re.findall(r'^(\S+).*?inet addr:(\S+).*?Mask:(\S+)', response, re.S | re.M)
            
            for i in ifaces:
                print '%s: %s/%s' % i
        
        else:
            raise ModuleException(self.name,  "No interfaces found")
                
        
