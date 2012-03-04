'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

classname = 'Name'
    
class Name(Module):
    '''Find files with matching name 
    (e=equal, ei= equal case insensitive , c= contains, ci= contains case insensitive)
    :find.name e|ei|c|ci <string> <start path> 
    '''
    
    
    vectors = VectorList([
       V('shell.php', 'php_recursive', """@swp('%s','%s','%s');
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
}"""),
       V('shell.sh', "find" , "find %s %s %s 2>/dev/null")
    ])
    

    params = ParametersList('Find files with matching name', vectors,
                    P(arg='match', help='Match if Equal, Equal case insensitive, Contains, Contains case insensitive', choices=['e', 'ei', 'c', 'ci'], pos = 0), 
                    P(arg='str', help='String to match', required=True, pos=1), 
                    P(arg='rpath', help='Remote starting path', default='.', required = True, pos=2)
                    )
    
    
    visible = True
    
    def __init__(self, modhandler, url, password):
        
        Module.__init__(self, modhandler, url, password)
        

    def __prepare_payload(self, vector, params):
        
        mod = params[0]
        match = params[1]
        path = params[2]
        
        str_mod = mod
        str_match = match
        str_path = path
        
        if vector.interpreter == 'shell.sh':

            if mod == 'e' or mod == 'c':
                str_mod = '-name' 
            elif mod == 'ei' or mod == 'ci':
                str_mod = '-iname'
            
            if mod == 'c' or mod == 'ci':
                str_match = '\'*' + str_match + '*\''

            
        return vector.payloads[0] % (str_path, str_mod, str_match)

            

    def run_module(self, match, str, rpath):
            
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            
            response = self.__execute_payload(vector, [match, str, rpath])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
        
        raise ModuleException(self.name,  "Files not found")
                    
                    
    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters)
    
        try:    
            response = self.modhandler.load(vector.interpreter).run({0 : payload})
        except ModuleException:
            response = None
        else:
            return response


        

    
    
    