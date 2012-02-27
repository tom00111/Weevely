'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
from core.enviroinment import Enviroinment
import readline, atexit, os, re, shlex

module_trigger = ':'
help_string = ':help'
cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )
    
            
class Terminal(Enviroinment):
    
    def __init__( self, modhandler, one_shot = False):

        self.modhandler = modhandler
        
        
        self.url = modhandler.url
        self.password = modhandler.password
        self.interpreter = modhandler.interpreter

        self.one_shot = one_shot
        
        self.matching_words = self.modhandler.help_completion('', only_name=True)
        self.completion_prefix = ''
    
        if not self.interpreter:
            print '[!] [shell.php] No remote backdoor found. Check URL and password.'
    
        elif not one_shot:
            
            
            Enviroinment.__init__(self)
        
            self.history      = os.path.expanduser( '~/.weevely_history' )

            try:
                
                readline.parse_and_bind( 'tab: menu-complete' )
                readline.set_completer( self.__complete )
                #readline.set_completion_display_matches_hook(self.__suggest)
                readline.read_history_file( self.history )
                
            except IOError:
                pass
    
            atexit.register( readline.write_history_file, self.history )


    def loop(self):
        
        while self.interpreter:
            
            prompt        = self._format_prompt()
                
            cmd       = raw_input( prompt )
            cmd       = cmd.strip()
            
            if cmd:
                if cmd[0] == module_trigger:
                    self.run_module_cmd(shlex.split(cmd))
                else:
                    self.run_line_cmd(cmd)
            
            
    def run_module_cmd(self, cmd_splitted):
        
        if not self.interpreter:
            return
             
        output = ''
    
        ## Help call
        if cmd_splitted[0] == help_string:
            modname = ''
            if len(cmd_splitted)>1:
                modname = cmd_splitted[1]
            print self.modhandler.helps(modname)
            
        else:
        
            if cmd_splitted[0][0] == ':':
                interpreter = cmd_splitted[0][1:]
                cmd_splitted = cmd_splitted[1:]
            else:
                interpreter = self.interpreter
                
            output =  self.run(interpreter, cmd_splitted)
   
        if output != None:
            print output       
            
    def run_line_cmd(self, cmd_line):
        
        if not self.interpreter:
            return
             
        output = ''
        
        if cmd_line == help_string:
            print self.modhandler.helps(cmd_line[len(help_string):])
            return
        
        if not self.one_shot:

            if self._handleDirectoryChange(cmd_line) == False:
                if self.interpreter == 'shell.php' and cmd_line.startswith('ls'):
                    print self.modhandler.load('shell.php').ls_handler(cmd_line)
                    return
                
                output = self.run(self.interpreter, [ cmd_line ])  
                
            else:
                pass
            
        else:
            output = self.run(self.interpreter, [ cmd_line ])  
            
        if output != None:
            print output
    

    def __suggest(substitution, matches, longest_match_length):
        print 'AHAAA'

#    def __complete( self, text, state ):
#
#            try:
#    
#                matches = self.modhandler.help_completion(text)
#                output = '\n%s\n%s' % ( '\n'.join(matches),  self._format_prompt())
#                print output
#                
#            except Exception, e:
#                print '[!] Error completing: %s' % e
#            
#            else:
#                return matches[state]

    def __complete( self, prefix, index ):
        
        try:
            if prefix != self.completion_prefix:
                self.matching_words = self.modhandler.help_completion(prefix, only_name=True)
                self.completion_prefix = prefix
            try:
                if index == 0:
                    print '\n%s' % ('\n'.join(self.modhandler.help_completion(prefix)))
                return self.matching_words[index]
            except IndexError:
                return None
        except Exception, e:
            print e
                

    def run(self, module_name, module_arglist):        
        
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
        
        if module_name not in self.modhandler.module_info.keys():
            print '[!] Error module with name \'%s\' not found' % (module_name)
        else:

            try:
                response = self.modhandler.load(module_name).run(arguments)
                if response != None:
                    return response
            except KeyboardInterrupt:
                print '[!] Stopped %s execution' % module_name
            except ModuleException, e:
                print '[!] [%s] Error: %s' % (e.module, e.error) 
        
      
    