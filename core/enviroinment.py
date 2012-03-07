'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
import readline, atexit, os, re, shlex


help_string = ':show'
cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )
respace = re.compile('.*\s+$', re.M)
set_string = ':set'
load_string = ':load'

class Enviroinment:
    
    
    def __init__(self):


            

        self.modhandler.set_verbosity(2)
        self.username = self.modhandler.load('system.info').run({ 0: "whoami" })
        self.hostname = self.modhandler.load('system.info').run({ 0: "hostname"})
        self.cwd = self.modhandler.load('system.info').run({ 0 : "basedir"})

        if 'shell.sh' in self.modhandler.loaded_shells:
            self.prompt = "%s@%s:%s$ "
        else:
            self.prompt = "%s@%s:%s (PHP)> "


        try:
            self.safe_mode = int(self.modhandler.load('system.info').run({ 0: "safe_mode" }))
        except:
            self.safe_mode = None
        else:
            if self.safe_mode:
                print '[!] Safe mode is enabled'
                
        self.modhandler.set_verbosity()
        
        print '\n[+] List modules with <tab> and show help with %s [module name]\n' % help_string
        
        self.matching_words =  self.modhandler.help_completion('') + [help_string, load_string, set_string]
        self.__init_completion()
             
 
    def __init_completion(self):
        
            try:
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind( 'tab: complete' )
                readline.set_completer( self.__complete )
                readline.read_history_file( self.configs.historyfile )
                
            except IOError:
                pass
            atexit.register( readline.write_history_file, self.configs.historyfile )


    def _format_prompt(self):
        
        return self.prompt % (self.username, self.hostname, self.cwd)
        
    
    def _handleDirectoryChange( self, cmd):
        
        cd  = cwd_extract.findall(cmd)
        
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
            
            if self.modhandler.load('shell.php').cwd_handler(path):
                self.cwd = path
            else:
                print "[!] Error changing directory to '%s', wrong path, incorrect permissions or safe mode enabled" % path

            return True

        return False    


    def __complete(self, text, state):
        """Generic readline completion entry point."""
        
        try:
            buffer = readline.get_line_buffer()
            line = readline.get_line_buffer().split()
            
            if ' ' in buffer:
                return []
            
            # show all commandspath
            if not line:
                all_cmnds = [c + ' ' for c in self.matching_words]
                if len(all_cmnds) > state:
                    return all_cmnds[state]
                else:
                    return []
                
            # account for last argument ending in a space
            if respace.match(buffer):
                line.append('')
            # resolve command to the implementation function
            
            cmd = line[0].strip()
            
            if cmd in self.matching_words:
                return [cmd + ' '][state]
            
            results = [c + ' ' for c in self.matching_words if c.startswith(cmd)] + [None]
            if len(results) == 2:
                if results[state]:
                    return results[state].split()[0] + ' '
                else:
                    return []
            return results[state]           
             
        except Exception, e:
            print '[!] Completion error: %s' % e
            import traceback
            traceback.print_exc()
            