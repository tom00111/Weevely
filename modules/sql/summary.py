'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random

classname = 'Summary'
 

    
class Summary(Module):
    '''Get SQL structure summary
    :sql.query mysql|postgres <host> <user> <pass> listdb | <db name>  
    '''
    
    vectors = VectorList( [
            Vector('sql.query', 'mysql', [ "SHOW DATABASES;", "SHOW TABLES FROM %s;", "SHOW COLUMNS FROM %s.%s;" ]) 
            ])



    def __init__( self, modhandler , url, password):
            
        self.structure = {}

        Module.__init__(self, modhandler, url, password)
        
        

    def run( self, mode, host, user, pwd , db ):

        vector = self._get_default_vector2()
        if vector:
            response = self.__execute_payload(vector, [mode, host, user, pwd, db])
            if response != None:
                return response
            
        vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells + [ 'sql.query' ])
        for vector in vectors:
            response = self.__execute_payload(vector, [mode, host, user, pwd, db])
            if response != None:
                return response
        
    def __execute_payload(self, vector, parameters):
        
        mode = parameters[0]
        host = parameters[1]
        user = parameters[2]
        pwd = parameters[3]
        db = parameters[4]
        
        if db == 'listdb':    
            # database
            payload = self.__prepare_payload(vector, [], 0) 
            response = self.modhandler.load(vector.interpreter).run(mode, host, user, pwd, payload)
            if response:
                for db in response.split('\n'):
                    self.structure[db]={}
                
                                
        
        else:      
            
            db = parameters[-1]
            self.structure[db] = {}
              
            # tables
            payload = self.__prepare_payload(vector, [db], 1) 
     
            response = self.modhandler.load(vector.interpreter).run(mode, host, user, pwd, payload)
            
            if response:
                for table in response.split('\n'):
                    
                    
                    self.structure[db][table]={}
                    
                    # columns
                    cpayload = self.__prepare_payload(vector, [db, table], 2) 
                    cresponse = self.modhandler.load(vector.interpreter).run(mode, host, user, pwd, payload)
                    if cresponse:
                        for column in response.split('\n'):   
                            self.structure[db][table][column]=[]
                                            
                    
        self.__print_db()

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
                
    
    
    