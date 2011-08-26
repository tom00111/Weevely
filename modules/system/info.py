'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Info'
    
class Info(Module):
    """Collect system shell informations
    ./weevely [ all | whoami | hostname | wd | doc_root ]
    """
    
    shell_vectors = { "whoami"       : "whoami",
                "hostname"     : "hostname",
                "basedir"   : "pwd"
                }
    
    php_vectors = {
                   "doc_root" : "print($_SERVER['DOCUMENT_ROOT']);"
    }
    

    def __init__( self, moddict , url, password):


        Module.__init__(self, moddict, url, password)
        
        moddict.load('system.exec', url, password)
        
        self.loaded = True
        
        self.infos = {}
        
                
    def run( self, info):
        
        
        if info == 'all':
            
            for info in self.shell_vectors:
                self.infos[info] = self.moddict['system.exec'].run(self.shell_vectors[info])
                
            for info in self.php_vectors:
                self.infos[info] = self.moddict['php.exec'].run(self.php_vectors[info])
                
        
        elif info in self.shell_vectors or info in self.php_vectors:
            if info in self.infos:
                return self.infos[info]
            else:
                if info in self.shell_vectors:
                    return self.moddict['system.exec'].run(self.shell_vectors[info])
                if info in self.php_vectors:
                    return self.moddict['php.exec'].run(self.php_vectors[info])
                    
            
        else:
            raise ModuleException("system.info",  "Information '%s' not supported." % (info))
        



    
    
    