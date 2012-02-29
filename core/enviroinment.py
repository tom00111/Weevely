'''
Created on 22/ago/2011

@author: norby
'''

from core.module import ModuleException
import readline, atexit, os, re, shlex


help_string = ':show'
cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )

class Enviroinment:
    
    
    def __init__(self):
        
        if self.interpreter == 'shell.sh':
            self.prompt = "%s@%s:%s$ "
        else:
            self.prompt = "%s@%s:%s php> "
            
        print '[+] List modules with <tab> and show help with %s [module name]\n' % help_string
            
        self.modhandler.set_verbosity(2)
        self.username = self.modhandler.load('system.info').run_module("whoami")
        self.hostname = self.modhandler.load('system.info').run_module("hostname")
        self.cwd = self.modhandler.load('system.info').run_module("basedir")

        try:
            self.safe_mode = int(self.modhandler.load('system.info').run_module("safe_mode"))
        except:
            self.safe_mode = None
        else:
            if self.safe_mode:
                print '[!] Safe mode is enabled'
                
        self.modhandler.set_verbosity()
 
 

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
                