'''
Created on 13/set/2011

@author: norby
'''


from core.module import Module, ModuleException

classname = 'Binaries'
    
class Binaries(Module):
    '''Enumerate available executables in common PATH folders
    :enumerate.binaries auto | <name> 
    '''

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

    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        
    def run( self, binary_name):
        
        path_list =  []
        
        if binary_name == 'auto':
            for bin in self.bins:
                for path in self.bins_path:
                    path_list.append(path + '/' + bin)
                    
        else:
            path_list = [ binary_name ]
            
        self.modhandler.load('enumerate.paths').run('', path_list)

            
        
