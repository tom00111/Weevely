'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Perms'
    
class Perms(Module):
    '''Find files by permission to write, read, execute
    :find.perms first|all file|dir|all w|r|x|all <path> 
    '''
    
    php_method = '''
@swp('%s','%s','%s','%s');
function ckmod($df, $m) { return ($m=="all")||($m=="w"&&is_writable($df))||($m=="r"&&is_readable($df))||($m=="x"&&is_executable($df)); }
function cktp($df, $f, $t) { return ($f!='.')&&($f!='..')&&($t=='all'||($t=='file'&&@is_file($df))||($t=='dir'&&@is_dir($df))); }
function swp($d, $type, $mod, $qty){
            $h = @opendir($d);
            while ($f = @readdir($h)) {
                    $df=$d.'/'.$f;
                    if(@cktp($df,$f,$type)&&@ckmod($df,$mod)) {
                            print($df."\\n");
                            if($qty=="first") return;
                    }
                    if(@cktp($df,$f,'dir')){
                            @swp($df, $type, $mod, $qty);
                    }
            }
            @closedir($h);
}
'''
    
    sh_method = "find %s %s %s %s 2>/dev/null"
    
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
        

    def __prepare_vector(self,interpreter, path, type, mod, qty):
        
        if interpreter == 'shell.sh':
            if qty == 'first':
                qty = '-print -quit'
            elif qty == 'all':
                qty = ''
            else:
                raise ModuleException("find.find",  "Find failed. Use first|all as first parameter.")
                
            if type == 'all':
                type = ''
            elif type == 'file':
                type = '-type f'
            elif type == 'dir':
                type = '-type d'
            else:
                raise ModuleException("find.find",  "Find failed. Use file|dir|all as second parameter.")
             
            if mod == 'all':
                mod = ''
            elif mod == 'w':
                mod = '-writable'
            elif mod == 'r':
                mod = '-executable'
            elif mod == 'x':
                mod = '-readable'
            else:
                raise ModuleException("find.find",  "Find failed. Use file|dir|all as second parameter.")
             
        
        
        return (path, type, mod, qty)

    def run(self, qty, type, mod, path):
            
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                    
                    payload = self.vectors[interpreter][vector] % self.__prepare_vector(interpreter, path, type, mod, qty)
                    print "[find.find] Finding file in %s using method '%s'" % (path, vector)  
                    
                    if interpreter == 'shell.sh':       
                        response = self.modhandler.load(interpreter).run(payload, False)
                    elif interpreter == 'shell.php':
                        response = self.modhandler.load(interpreter).run(payload)
                        
                    if response:
                        return response
                
                
        raise ModuleException("find.find",  "Find failed.")
            

        

    
    
    