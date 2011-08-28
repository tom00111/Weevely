'''
Created on 22/ago/2011

@author: norby
'''

from inspect import getargspec

class_name = 'Module'


class Module:
    '''Generic class Module to inherit'''
    
    visible = True
    
    def __init__(self, modhandler, url, password):
        self.modhandler = modhandler
        self.url = url
        self.password = password
        
        self._probe()
        self.__get_arguments_num()
    
    def _probe(self):
        pass
    
    def run(self):
        pass
    
    def __get_arguments_num(self):
        
        len_module_arguments = len(getargspec(self.run).args) - 1
        if getargspec(self.run).defaults: 
            len_module_arguments -= len(getargspec(self.run).defaults)
        self.len_arguments = len_module_arguments
    
class ModuleException(Exception):
    def __init__(self, module, value):
        self.module = module
        self.error = value
    def __str__(self):
        return self.error