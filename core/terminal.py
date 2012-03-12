'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
from core.enviroinment import Enviroinment
from core.configs import Configs, dirpath, rcfilepath
import os, re, shlex

module_trigger = ':'
help_string = ':show'
set_string = ':set'
load_string = ':load'

            
class Terminal(Enviroinment):
    
    def __init__( self, modhandler, one_shot = False):

        self.modhandler = modhandler
        
        
        self.url = modhandler.url
        self.password = modhandler.password

        self.one_shot = one_shot

        self.configs = Configs()
        self.__load_rcfile(dirpath + rcfilepath)
    
        if not one_shot:
            Enviroinment.__init__(self)


    def loop(self):
        
        while True:
            
            prompt        = self._format_prompt()
                
            cmd       = raw_input( prompt )
            cmd       = cmd.strip()
            
            if cmd:
                if cmd[0] == module_trigger:
                    self.run_module_cmd(shlex.split(cmd))
                else:
                    self.run_line_cmd(cmd)
            
            
    def run_module_cmd(self, cmd_splitted):
        
        output = ''
    
        ## Help call
        if cmd_splitted[0] == help_string:
            modname = ''
            if len(cmd_splitted)>1:
                modname = cmd_splitted[1]
            print self.modhandler.helps(modname),
               
        ## Set call
        elif cmd_splitted[0] == set_string:            
            if len(cmd_splitted)>2:
                modname = cmd_splitted[1]
                self.set(modname, cmd_splitted[2:])
           
        ## Load call
        elif cmd_splitted[0] == load_string:   
            if len(cmd_splitted)>=2:
                self.__load_rcfile(cmd_splitted[1])
                           
        ## Command call    
        else:

            interpreter = None
            if cmd_splitted[0][0] == module_trigger:
                interpreter = cmd_splitted[0][1:]
                cmd_splitted = cmd_splitted[1:]
                
                
            output =  self.run(interpreter, cmd_splitted)
   
        if output != None:
            print output       
            
    def run_line_cmd(self, cmd_line):
        
        output = ''
        
        if not self.one_shot:

            if self._handleDirectoryChange(cmd_line) == False:
                if 'shell.sh' not in self.modhandler.loaded_shells and cmd_line.startswith('ls'):
                    print self.modhandler.load('shell.php').ls_handler(cmd_line)
                    return
                
                output = self.run(None, [ cmd_line ])  
                
            else:
                pass
            
        else:
            output = self.run(None, [ cmd_line ])  
            
        if output != None:
            print output
    

    def __format_arglist(self, module_arglist):
        
        arguments = {}
        pos = 0
        for arg in module_arglist:
            if '=' in arg:
                name, value = arg.split('=')
            else:
                name = pos
                value = arg
                
            arguments[name] = value
            pos+=1
        
        return arguments


    def set(self, module_name, module_arglist):
        
        if module_name not in self.modhandler.module_info.keys():
            print '[!] Error module with name \'%s\' not found' % (module_name)
        else:
           arguments = self.__format_arglist(module_arglist)
           module_class = self.modhandler.load(module_name, init_module=False)
           
           check, params = module_class.params.set_and_check_parameters(arguments, oneshot=False)
           
            
           erroutput = '[%s] ' % module_name
           if not check:
               erroutput += 'Error setting parameters. '
               
           print '%sValues: %s' % (erroutput, module_class.params.param_summary()),

 
    def run(self, module_name, module_arglist):        
        
        # TODO: use directly load_interpreters or get_best_interpreter
        # The double choose of best inetrpreter and load_inerpreter call seems
        # Redundant
        
        if module_name == None:
            
            if not self.modhandler.interpreter:
                self.modhandler.load_interpreters()
            
            if 'shell.sh' in self.modhandler.loaded_shells:
                module_name = 'shell.sh'
            else:
                module_name = 'shell.php'
            
            
        if module_name not in self.modhandler.module_info.keys():
            print '[!] Error module with name \'%s\' not found' % (module_name)
        else:
            arguments = self.__format_arglist(module_arglist)
        
            try:
                response = self.modhandler.load(module_name).run(arguments)
                if response != None:
                    return response
            except KeyboardInterrupt:
                print '[!] Stopped %s execution' % module_name
            except ModuleException, e:
                print '[!] [%s] Error: %s' % (e.module, e.error) 
           

    def __load_rcfile(self, path = None):
        
        if path:
            for cmd in self.configs.read_rc(os.path.expanduser(path)):
                
                cmd       = cmd.strip()
                
                if cmd:
                    print '[rc] %s' % (cmd)
                    
                    if cmd[0] == module_trigger:
                        self.run_module_cmd(shlex.split(cmd))
                    else:
                        self.run_line_cmd(cmd)    
    
        
        