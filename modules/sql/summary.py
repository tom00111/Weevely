'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random
from core.parameters import ParametersList, Parameter as P

classname = 'Summary'
 

    
class Summary(Module):
    '''Get SQL database summary
    :sql.summary mysql|postgres <host> <user> <pass> <db name>  
    '''
    
    vectors = VectorList( [
            Vector('sql.query', 'mysql', [ "SHOW DATABASES;", "SHOW TABLES FROM %s;", "SHOW COLUMNS FROM %s.%s;" ]) 
            ])

    params = ParametersList('Get SQL summary of database or single tables', vectors,
            P(arg='dbms', help='DBMS', choices=['mysql'], required=True, pos=0),
            P(arg='user', help='SQL user to bruteforce', required=True, pos=1),
            P(arg='pwd', help='SQL password', required=True, pos=2),
            P(arg='db', help='Database name', required=True, pos=3),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=4))


    def __init__( self, modhandler , url, password):
            
        self.structure = {}

        Module.__init__(self, modhandler, url, password)
        
        

    def run_module( self, mode, user, pwd , db, host ):

        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells + [ 'sql.query' ])
        for vector in vectors:
            response = self.__execute_payload(vector, [mode, host, user, pwd, db])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
        
    def __execute_payload(self, vector, parameters):
        
        mode = parameters[0]
        host = parameters[1]
        user = parameters[2]
        pwd = parameters[3]
        db = parameters[4]
        
        self.modhandler.set_verbosity(2)
        
        self.structure[db] = {}
          
        # tables
        payload = self.__prepare_payload(vector, [db], 1) 
 
        response = self.modhandler.load(vector.interpreter).run({'dbms' : mode, 'user' : user, 'pwd': pwd, 'query' : payload, 'host' : host})
        
        if response:
            for table in response.split('\n'):
                
                
                self.structure[db][table]={}
                
                # columns
                cpayload = self.__prepare_payload(vector, [db, table], 2) 
                #cresponse = self.modhandler.load(vector.interpreter).run_module(mode, user, pwd, payload, host)
                
                cresponse = self.modhandler.load(vector.interpreter).run({'dbms' : mode, 'user' : user, 'pwd': pwd, 'query' : payload, 'host' : host})
        
                if cresponse:
                    for column in response.split('\n'):   
                        self.structure[db][table][column]=[]
                                            
        self.modhandler.set_verbosity()
        
        if self.structure[db]:
            self.__print_db()
        else:
            self.mprint('[%s] Error getting database structure, no response' % (self.name))

    def __prepare_payload( self, vector, parameters , parameter_num):

        if vector.payloads[parameter_num].count( '%s' ) == len(parameters):
            return vector.payloads[parameter_num] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        

    def __print_db(self):
        
        for db in self.structure:
            
            print 'DB \'%s\'' % db
            
            for table in self.structure[db]:
                print 'TABLE: ' + table 
                
                print '|',
                for column in self.structure[db][table]:
                    print column + ' |',
                    
                print ''
                
    
    
    