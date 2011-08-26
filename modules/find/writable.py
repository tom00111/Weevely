'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
import random

classname = 'Writable'
    
class Writable(Module):
    '''Find writable dirs and files
    find.writable < first | all > <file | dir | all> <'path' | .> 
    '''
    
    vectors = {
            "all" : "find %s -perm -2 %s 2>/dev/null",
            "file" : "find %s -perm -2 -type f %s 2>/dev/null",
            "dir" : "find %s -perm -2 -type d %s 2>/dev/null"
              }
    
    visible = True
    
    
    def __init__(self, moddict, url, password):
        
        Module.__init__(self, moddict, url, password)
        
        moddict.load('system.exec', url, password)

    def run(self, qty, mode, path):
        
        if not mode in self.vectors.keys():
            raise ModuleException("find.writable",  "Find failed. Use < file | dir | all > as 2nd parameter.")
        
        if qty == 'first':
            qty_string = '-print -quit'
        elif qty == 'all':
            qty_string = ''
        else:
            raise ModuleException("find.writable",  "Find failed. Use < first | all > as first parameter.")
            
        payload = self.vectors[mode] % (path, qty_string)
        
        return self.moddict['system.exec'].run(payload, False)
            

        

    
    
    