'''
Created on 13/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.parameters import ParametersList, Parameter as P

classname = 'Binaries'
    
class Binaries(Module):
    '''Enumerate binaries in common PATH folders
    :enum.binaries auto | <name> 
    '''


    params = ParametersList('Enumerate available binaries in common PATH folders', None,
                    P(arg='name', help='Search binary name, or \'auto\' for common binaries', pos=0, default='auto'), 
                    )

    bins_path = [ "/usr/bin",
             "/usr/local/bin",
             "/bin",
             "/usr/local/sbin",
             "/usr/sbin",
             "/sbin",
             "/usr/bin/X11"
             ]
    
    bins = { 'wget' : '',
             'gcc' : '', 
             'ifconfig' : '', 
             'arp' : '', 
             'ip' : '', 
             'locate' : '', 
             'lastlogin' : '', 
             'iptables' : '', 
             'netstat' : '',
             'telnet' : '', 
             'ssh' : '', 
             'mysql' : '',
             'nc' : ''
             }
        
    def run_module( self, binary_name):
        
        path_list =  []
        
        if binary_name == 'auto':
            for bin in self.bins:
                for path in self.bins_path:
                    path_list.append(path + '/' + bin)
                    
        else:
            for path in self.bins_path:
                path_list.append(path + '/' + binary_name)
            
        if path_list:
            self.modhandler.load('enum.paths').run_module('',  list=path_list)

