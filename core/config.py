'''
Created on 30/ago/2011

@author: norby
'''
import os
from ConfigParser import RawConfigParser, NoSectionError


class Config:
    
    def __init__(self, module_names):
        
        
        self.conf = RawConfigParser()
        self.conf_path = os.path.expanduser( '~/.weevely.ini' )
        
        if os.path.exists(self.conf_path):
            self.conf.read(self.conf_path)
            
        else:
            print '[!] Config file \'%s\' not found, creating' % (self.conf_path)
            self.__write_conf(module_names)
            
            
    def __write_conf(self, module_names):
            
        for name in module_names:
            self.conf.add_section(name)
            self.conf.set(name, 'default_vector', '')
            
        self.conf.add_section('global')
        self.conf.set('global','http_proxy','')
        self.conf.set('global','request_mode','')
            
        with open(self.conf_path, 'wb') as configfile:
            self.conf.write(configfile)
            
    
    def get_option(self, section, option):
        try:
            return self.conf.get(section,option)
        except NoSectionError:
            pass
            #print '[!] No section \'%s\' in config file.' % section
        
    def get_vector(self, section):
        try:
            return self.conf.get(section,'default_vector')
        except NoSectionError:
            pass
            #print '[!] No section \'%s\' in config file' % section
        
            

        
    