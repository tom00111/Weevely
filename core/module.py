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
        
        self.name = self.__module__[8:]
        
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
        
    def _get_default_vector(self):
        
        default_interpreter = None
        default_vector = None
        
        conf_interpreter, conf_vector = self.modhandler.conf.get_vector(self.name)
        if conf_interpreter in self.vectors:
            default_interpreter = conf_interpreter
            if conf_vector in self.vectors[conf_interpreter]:
                default_vector = conf_vector
        
        return default_interpreter, default_vector
    
class ModuleException(Exception):
    def __init__(self, module, value):
        self.module = module
        self.error = value
    def __str__(self):
        return self.error