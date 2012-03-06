"$f='%s'; (file_exists($f) || is_readable($f) || is_writable($f) || is_file($f) || is_dir($f)) && print(1);"'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

classname = 'Check'
    
class Check(Module):
    '''Check remote files type, md5 and permission'''
    
    
    vectors = VectorList([
    V('shell.php', 'exists', "$f='%s'; (file_exists($f) || is_readable($f) || is_writable($f) || is_file($f) || is_dir($f)) && print(1);",),
       V('shell.php', "dir" , "is_dir('%s') && print(1);"),
       V('shell.php', "md5" , "print(md5_file('%s'));"),
       V('shell.php',  "r", "is_readable('%s') && print(1);"),
       V('shell.php', "w", "is_writable('%s') && print(1);"),
       V('shell.php',  "x", "is_executable('%s') && print(1);"),
       V('shell.php', "file", "is_file('%s') && print(1);")
    ])
    

    params = ParametersList('Check remote files type, md5 and permission', [],
                    P(arg='rpath', help='Choose remote file path', required=True, pos=0),
                    P(arg='mode', help='Choose mode', required=True, choices=vectors.get_names_list(), pos=1))
    
    
    def run_module(self, remote_path, mode):
        
        # Skip default vector load, here vector=mode
        
        vector  = self.vectors.get_vector_by_name(mode)
    
        response = self.__execute_payload(vector, [remote_path, mode])
        if response != None:
            return response
    

    def __execute_payload(self, vector, parameters):
        
        remote_path = parameters[0]
        mode = parameters[1]
        
        payload = self.__prepare_payload(vector, [remote_path])
    
        try:    
            response = self.modhandler.load(vector.interpreter).run({ 0 : payload})
        except ModuleException:
            response = None
        else:
            
            if response == '1':
                return True
            elif (mode == 'md5' and response):
                return response
            else:
                if mode != 'exists':
                    if not self.run({'rpath' : remote_path, 'mode' :  'exists'}):
                        self.mprint('File does not exists', 4)
                    
            return False
            

        raise ModuleException(self.name,  "File check failed")
                
        
    def __prepare_payload( self, vector, parameters ):


        if vector.payloads[0].count( '%s' ) == len(parameters):
            return vector.payloads[0] % tuple(parameters)
        else:
            raise ModuleException(self.name,  "Error payload parameter number does not corresponds")
        