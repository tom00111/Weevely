'''
Created on 13/set/2011

@author: norby
'''


from core.module import Module, ModuleException

classname = 'Binaries'
    
class Binaries(Module):
    '''Find executables in common PATH folders
    :find.binaries all | <name> 
    '''

    paths = [ "/usr/local/bin",
             "/usr/bin",
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
        
        self.vector = "(is_file('%s') && print(1)) || (is_executable('%s') && print(2));"
        
        Module.__init__(self, modhandler, url, password)
        
        
    def run( self, binary_name):
        
        

        if binary_name == 'all':
            
            
            output=''
            
            for bin in self.bins:
                
                tabs = '\t'*(3-((len(bin)+1)/8))    
                output += '%s:' % bin
                
                for path in self.paths:
                         
                    completepath = path + '/' + bin
                         
                    filemode = self.modhandler.load('shell.php').run(self.vector % ( completepath, completepath ))
                    filemode_str = ''
                        
                    if filemode == '1' or filemode == '2':
                        
                        if filemode == '1':
                            filemode_str = 'Executable'
                        else:
                            filemode_str = 'Not Executable'
                            
                        self.bins[bin] = completepath
                        output += '%s%s%s%s' % (tabs, completepath, tabs, filemode_str)
                        break
                    
                output += '\n'
                    
                         
                        

                    
                    
            return output
        
        elif binary_name in self.bins and self.bins['binary_name']:
            return self.bins[path]
        
        else:
            for path in self.paths:
                completepath = path + '/' + binary_name
                filemode = self.modhandler.load('shell.php').run(self.vector % ( completepath, completepath ))
                    
                filemode_str = '' 
                if filemode == '1':
                    filemode_str = 'Executable'
                    self.bins[binary_name] = completepath
                elif filemode == '2':
                    filemode_str = 'Not Executable'
                    self.bins[binary_name] = completepath
                                        
                return '%s:\t%s\t%s\n' % (bin, self.bins[binary_name], filemode_str)
         
        raise ModuleException(self.name,  "Executable binary '%s' not found." % (binary_name))

        
