'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
import readline, atexit, os, re, shlex

class Terminal():
    
    def __init__( self, modhandler, one_shot = False):

        self.modhandler = modhandler
        
        self.url = modhandler.url
        self.password = modhandler.password
        self.interpreter = None
        self.module_string = ':module'
        self.help_string = ':help'
        self.one_shot = one_shot
        self.completions = {}
                
        self.__get_best_interpreter_available()
        
        if not one_shot:
            
            self.history      = os.path.expanduser( '~/.weevely_history' )

            try:
                readline.parse_and_bind( 'tab: menu-complete' )
                readline.set_completer( self.__complete )
                readline.read_history_file( self.history )
            except IOError:
                pass
    
            atexit.register( readline.write_history_file, self.history )


    def __get_best_interpreter_available(self):
        
        for shell_name in self.modhandler.module_info:
            if shell_name.startswith('shell.'):
        
                try:
                    self.modhandler.load(shell_name)
                except ModuleException, e:
                    print '[!] [%s] Error loading module: %s' % (shell_name, e)
                else:
                    self.interpreter = shell_name
                    break

        if self.interpreter == 'shell.sh':
            
            self.username      = self.modhandler.load('system.info').run("whoami")
            self.hostname      = self.modhandler.load('system.info').run("hostname")
            self.cwd           = self.modhandler.load('system.info').run("basedir")
            self.cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )
            self.prompt = "[shell.sh] %s@%s:%s$ "
            print '[+] Using system shell interpreter \'%s\'' % self.interpreter
            
        elif self.interpreter == 'shell.php':
            print '[+] Fallback to PHP interpreter \'%s\'.' % self.interpreter
            self.prompt        = "[shell.php]$ "
            
        else:
            print '[!] No backdoor found. Check url and password'
            

    def loop(self):
        
        while self.interpreter:
            
            if self.interpreter == 'shell.sh':
                prompt        = self.prompt % (self.username, self.hostname, self.cwd)
            else:
                prompt = self.prompt
                
            cmd       = raw_input( prompt )
            cmd       = cmd.strip()
            
            if cmd:
                self.run_single(shlex.split(cmd))
            
    def run_single(self, cmd_split):
    
        if not self.interpreter:
            return
            
        output = ''
        if cmd_split[0] == self.module_string:
            if len(cmd_split)==2:
                output = self.run_module(cmd_split[1], [])
            elif len(cmd_split)==3:
                output =  self.run_module(cmd_split[1], [ cmd_split[2] ])
            elif len(cmd_split)>3:
                output =  self.run_module(cmd_split[1], cmd_split[2:])
            else:
                print '[!] Error specify module name'
                
        elif cmd_split[0] == self.help_string:
            
            print ''
            for mod_name in self.modhandler.module_info:
                if self.modhandler.module_info[mod_name][0]:
                    print "%s: %s" % (mod_name, self.modhandler.module_info[mod_name][1])
            
            
        elif cmd_split[0] != self.module_string:
        
            cmd = ' '.join(cmd_split)
        
            if self.interpreter == 'shell.sh' and not self.one_shot: 
                if self.__handleDirectoryChange(cmd) == False:
                    readline.add_history(cmd)
                    cmd = "cd %s && %s" % ( self.cwd, cmd )  
                else:
                    cmd = "cd %s" % ( self.cwd )     
                    
            output = self.run_module(self.interpreter, [ cmd ])  
            
        if output:
            print output
    


    def __handleDirectoryChange( self, cmd ):
        cd  = self.cwd_extract.findall(cmd)
        
        if cd != None and len(cd) > 0:    
            cwd  = cd[0].strip()
            path = self.cwd
            if cwd[0] == '/':
                path = cwd
            elif cwd == '..':
                dirs = path.split('/')
                dirs.pop()
                path = '/'.join(dirs)
            elif cwd == '.':
                pass
            elif cwd[0:3] == '../':
                path = cwd.replace( '../', path )
            elif cwd[0:2] == './':
                path = cwd.replace( './', path )
            else:
                path = (path + "/" + cwd).replace( '//', '/' ) 
            
            exists = self.run_module('system.exec', [ "( [ -d '%s' ] && echo 1 ) || echo 0" % path ])
            if exists == "1":
                self.cwd = path
                    
            else:
                print "[!] Directory '%s' does not exist or is not accessible." % path

            return True

        return False

    def __complete( self, text, state ):
        try:
            matches = self.completions[text]
        except KeyError:
            matches = []
            items   = readline.get_current_history_length()
            for i in range( items ):
                item = readline.get_history_item(i)
                if item != None and text in item:
                    matches.append(item)
        
            self.completions[text] = matches
        
        try:
            return matches[state]
        except IndexError:
            return None


    def run_module(self, module_name, module_arguments):
        
        if module_name not in self.modhandler.module_info.keys():
            print '[!] [%s] Error module not found' % (module_name)
        else:
            try:
                module_arguments_requested = self.modhandler.load(module_name).len_arguments
            except ModuleException, e:
                print '[!] [%s] Error while loading: %s' % (e.module, e)   
            
            else: 
                if module_arguments_requested != len(module_arguments): 
                    print '[!] [%s] Error module needs %i arguments (not %i), printing documentation:\n' % (module_name, module_arguments_requested, len(module_arguments))
                    if self.modhandler.module_info[module_name][0]: print '%s: %s' % (module_name, self.modhandler.module_info[module_name][1])
                
                else:
                    try:
                        return self.modhandler.load(module_name).run(*module_arguments)
                    except ModuleException, e:
                        print '[!] [%s] Error: %s' % (e.module, e) 
        
      
    
    
    