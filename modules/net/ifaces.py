'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P
import re
from external.ipaddr import IPNetwork


classname = 'Ifaces'
    
class Ifaces(Module):

    params = ParametersList('Print network interfaces IP/mask', [])

    def __init__(self, modhandler, url, password):
        self.ifaces = {}
        
        Module.__init__(self, modhandler, url, password)    
    
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
            
            if ifaces:
                
                for i in ifaces:
                    ipnet = IPNetwork('%s/%s' % (i[1], i[2]))
                    self.ifaces[i[0]] = ipnet
                    self.mprint('%s: %s' % (i[0], ipnet))
        
        else:
            raise ModuleException(self.name,  "No interfaces infos found")
                
        
