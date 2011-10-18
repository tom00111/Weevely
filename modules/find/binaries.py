'''
Created on 13/set/2011

@author: norby
'''


from core.module import Module, ModuleException

classname = 'Binaries'
    
class Binaries(Module):
    '''Find executables in common PATH folders
    :find.binaries auto | <name> 
    '''

    paths = [ "/usr/bin",
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
        
        
    def __checkfile(self, bin, completepath):
        
        output = None
             
        if self.modhandler.load('file.check').run(completepath, 'x' , True):
            output = 'Executable'
            self.bins[bin] = completepath  
        elif self.modhandler.load('file.check').run(completepath, 'exists', True ):
            output = 'Not Executable'
            self.bins[bin] = completepath  

        return output

        
    def run( self, binary_name):
        
        found = False
        if binary_name == 'auto':
            
            for bin in self.bins:
                
                output = bin + ':' + '\t'*(3-((len(bin)+1)/8))
                print output,
                
                for path in self.paths:
                    
                    completepath = path + '/' + bin
                    
                    response = self.__checkfile(bin, completepath)
                    if response:
                        print completepath, response,
                        found = True
                        break
                    
                print ''
                    
        elif binary_name in self.bins and self.bins[binary_name]:
            return self.bins[path]
        else:
            for path in self.paths:
                    
                completepath = path + '/' + binary_name
                
                response = self.__checkfile(binary_name, completepath)
                if response:
                    return completepath
            
        if not found:        
            raise ModuleException(self.name,  "Binary '%s' not found." % (binary_name))

        
