'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

classname = 'Perms'
    
class Perms(Module):
    '''Find files with write, read, execute permissions
    :find.perms first|all file|dir|all w|r|x|all <path> 
    '''

    vectors = VectorList([
       V('shell.php', 'php_recursive', """@swp('%s','%s','%s','%s');
function ckmod($df, $m) { return ($m=="any")||($m=="w"&&is_writable($df))||($m=="r"&&is_readable($df))||($m=="x"&&is_executable($df)); }
function cktp($df, $f, $t) { return ($f!='.')&&($f!='..')&&($t=='any'||($t=='f'&&@is_file($df))||($t=='d'&&@is_dir($df))); }
function swp($d, $type, $mod, $qty){
$h = @opendir($d);
while ($f = @readdir($h)) {
$df=$d.'/'.$f;
if(@cktp($df,$f,$type)&&@ckmod($df,$mod)) {
print($df."\\n");
if($qty=="first") return;
}
if(@cktp($df,$f,'d')){
@swp($df, $type, $mod, $qty);
}
}
@closedir($h);
}"""),
       V('shell.sh', "find" , "find %s %s %s %s 2>/dev/null")
    ])
    

    params = ParametersList('Find files by permissions', vectors,
                    P(arg='qty', help='How many files display', choices=['first', 'any'], default='any'), 
                    P(arg='type', help='Type', choices=['f','d', 'any'], default='any'), 
                    P(arg='perm', help='Permission', choices=['w','r','x','any'], default='r'),
                    P(arg='rpath', help='Remote starting path', default='.')
                    )
    
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        

    def __prepare_payload( self, vector, parameters ):  

        path = parameters[0]
        qty = parameters[1]
        type = parameters[2]
        mod = parameters[3]
            
        if vector.interpreter == 'shell.sh':
            if qty == 'first':
                qty = '-print -quit'
            elif qty == 'any':
                qty = ''
                
            if type == 'any':
                type = ''
            elif type == 'f':
                type = '-type f'
            elif type == 'd':
                type = '-type d'
             
            if mod == 'any':
                mod = ''
            elif mod == 'w':
                mod = '-writable'
            elif mod == 'r':
                mod = '-readable'
            elif mod == 'x':
                mod = '-executable'
            
        return vector.payloads[0] % (path, type, mod, qty)
        

    def run_module(self, qty, type, mod, path):
            
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            
            response = self.__execute_payload(vector, [path, qty, type, mod])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
        
        raise ModuleException(self.name,  "Files not found")
                    
                    
    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters)
    
        try:    
            response = self.modhandler.load(vector.interpreter).run({ 0 : payload })
        except ModuleException:
            response = None
        else:
            return response

        
                
        

    
    
    