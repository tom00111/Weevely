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
    
    def mprint(self, str, importance = 3):
        if importance <= self.modhandler.verbosity:
            print str
        
    
    def _probe(self):
        pass
    
    def run(self, args = {}):
        
        output = None
        check1 = self.params.set_check_args(args)
        if check1:

            check2, arglist = self.params.get_check_args_list()
            
            if check2:
                output = self.run_module(*arglist)
                self.params.clean()
        
        return output
    
    def __get_arguments_num(self):
        
        len_module_arguments = len(getargspec(self.run).args) - 1
        if getargspec(self.run).defaults: 
            len_module_arguments -= len(getargspec(self.run).defaults)
        self.len_arguments = len_module_arguments
        
    def _get_default_vector(self):
        
        conf_vector = self.modhandler.conf.get_vector(self.name)
        
        for conf_interpreter in self.vectors:
            if conf_vector in self.vectors[conf_interpreter]:
                return conf_interpreter, conf_vector
    
        return None, None
    
    def _get_default_vector2(self):
        
        conf_vector = self.params.get_parameter_value('vector')
        
        if not conf_vector:
            conf_vector = self.modhandler.conf.get_vector(self.name)
        
        vector = self.vectors.get_vector_by_name(conf_vector)
        
        
        if vector:
            return [ vector ]
        
        return []
    
class ModuleException(Exception):
    def __init__(self, module, value):
        self.module = module
        self.error = value
    def __str__(self):
        return self.error