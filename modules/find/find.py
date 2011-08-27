'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Find'
    
class Find(Module):
    '''Find writable|readable|executable|all file for current user
    find.file first|all file|dir|all w|r|x|all <path> 
    '''
    
    php_method = '''
@swp(%s,%s,%s',%s);
function ckmod($df, $m) { return ($m=="all")||($m=="w"&&is_writable($df))||($m=="r"&&is_readable($df))||($m=="x"&&is_executable($df)); }
function cktp($df, $f, $t) { return ($f!='.')&&($f!='..')&&($t=='all'||($t=='file'&&@is_file($df))||($t=='dir'&&@is_dir($df))); }
function swp($d, $qty, $type, $mod){
            $h = @opendir($d);
            while ($f = @readdir($h)) {
                    $df=$d.'/'.$f;
                    if(@cktp($df,$f,$type)&&@ckmod($df,$mod)) {
                            print($df."\n");
                            if($qty=="first") die();
                    }
                    if(@cktp($df,$f,'dir')){
                            @swp($df, $qty, $type, $mod);
                    }
            }
            @closedir($h);
}
    '''
    
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
        

    def __prepare_vector(self,interpreter, qty,type,mod):
        
        if interpreter == 'shell.sh':
            if qty == 'first':
                qty_string = '-print -quit'
            elif qty == 'all':
                qty_string = ''
            else:
                raise ModuleException("find.writable",  "Find failed. Use first|all as first parameter.")
                
            if type == 'all':
                type_string = ''
            elif type == 'file':
                type_string = '-type f'
            elif type == 'dir':
                type_string = '-type d'
            else:
                raise ModuleException("find.writable",  "Find failed. Use file|dir|all as second parameter.")
             
            if mod == 'all':
                mod_string = ''
            elif mod == 'w':
                mod_string = '-writable'
            elif mod == 'r':
                mod_string = '-executable'
            elif mod == 'x':
                mod_string = '-readable'
            else:
                raise ModuleException("find.writable",  "Find failed. Use file|dir|all as second parameter.")
             
            return (qty_string, type_string, mod_string)
        
        elif interpreter == 'shell.php':
            return (qty, type, mod)
        

    def run(self, qty, type, mod, path):
        

            
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                
                    payload = self.vectors[interpreter][vector] % self.__prepare_vector(interpreter, qty, type, mod)
                    print "[find.writable] File read using method '%s'" % (self.vector)  
                                     
                    return self.modhandler.load(interpreter).run(payload, False)
                
        raise ModuleException("find.writable",  "Find failed.")
            

        

    
    
    