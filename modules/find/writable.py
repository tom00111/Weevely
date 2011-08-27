'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
import random

classname = 'Writable'
    
class Writable(Module):
    '''Find writable dirs and files for current user
    find.writable first|all file|dir|all <path> 
    '''
    
    php_method = '''
        @swp('%s','%s','%s');
        function swp($d, $qty, $mod){
            $h = @opendir($d);
            while ($f = @readdir($h)) {
                    $df=$d.'/'.$f;
                    if(($mod=='file'||$mod=='all')&&(@is_file($df))&&@is_writable($df)) {
                            print($df."\n");
                            if($qty=="first") die();
                    }
                    if((@is_dir($df))&&($f!='.')&&($f!='..')){
                            if(($mod=='dir'||$mod=='all')&&@is_writable($df)) {
                                    print($df."\n");
                                    if($qty=="first") die();
                            }
                            @swp($df, $qty, $mod);
                    }
            }
            @closedir($h);
    }'''
    
    sh_method = "find %s -writable %s %s 2>/dev/null"
    
    vectors = {
               "shell.sh" : {
                             'find' : sh_method
                },
               
               "shell.php" : {
              "php_recursive_find" : php_method
                              }
          }
    
    visible = True
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        

    def run(self, qty, type, path):
        
        if qty == 'first':
            qty_sh_string = '-print -quit'
        elif qty == 'all':
            qty_sh_string = ''
        else:
            raise ModuleException("find.writable",  "Find failed. Use first|all as first parameter.")
            
        if type == 'all':
            type_sh_string = ''
        elif type == 'file':
            type_sh_string = '-type f'
        elif type == 'dir':
            type_sh_string = '-type d'
        else:
            raise ModuleException("find.writable",  "Find failed. Use file|dir|all as second parameter.")
         
            
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                
                    payload = self.vectors[interpreter][vector] % (path, qty_sh_string, type_sh_string)     
                    print "[find.writable] File read using method '%s'" % (self.vector)  
                                     
                    return self.modhandler.load(interpreter).run(payload, False)
                
        raise ModuleException("find.writable",  "Find failed.")
            

        

    
    
    