'''
Created on 30/ago/2011

@author: norby
'''
import os
from ConfigParser import RawConfigParser


class Config:
    
    def __init__(self, module_names, conf_path='~/.weevely.ini'):
        
        self.conf = RawConfigParser()
        self.conf_path = conf_path
        
        if os.path.exists(conf_path):
            self.conf.read(self.conf_path)
            
        else:
            print '[!] Config file \'%s\' not found, creating new' % (conf_path)
            self.__write_conf(module_names)
            
            
    def __write_conf(self, module_names):
            
        for name in module_names:
            self.conf.add_section(name)
            self.conf.set(name, 'default_interpreter','')
            self.conf.set(name, 'default_vector', '')
            
        self.conf.add_section('global')
        self.conf.set('global','http_proxy','')
            
        with open(self.conf_path, 'wb') as configfile:
            self.conf.write(configfile)
            
    
    def get_option(self, section, option):
        return self.conf.get(section,option)
        
    def get_vector(self, section):
        return self.conf.get(section,'default_interpreter'), self.conf.get(section,'default_vector')
        
        
            

        
    