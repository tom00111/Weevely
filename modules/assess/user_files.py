

from core.module import Module, ModuleException

classname = 'UserFiles'

class UserFiles(Module):
    """Enumerate user files. Search common ones in home, public_html, specify file path or load a file list
    :assess.user_files all | home | web | <file> | load:<file_list.txt>
    """
    
    
    common_files = { 
                    
                    "home" : [ ".bashrc", 
                              ".bash_history", 
                              ".profile",
                              ".ssh",
                              ".ssh/authorized_keys",
                              ".ssh/known_hosts"
                              ],
                    "web" : [ "public_html/", 
                             "public_html/wp-config.php", 
                             "public_html/config.php", 
                             "public_html/uploads",
                             "public_html/.htaccess" ] 
                    
                    }

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run(self, mode):
        
        if mode != 'all' and mode not in self.common_files.keys():
            
            if mode.startswith('load:'):
                try:
                    custom_files=open(mode[5:],'r').read().splitlines()
                except:
                    raise ModuleException(self.name,  "Error opening path list \'%s\'" % mode[5:])
            else:
                custom_files = mode.split(',')
                
            if custom_files:
                self.common_files['custom'] = custom_files
                mode = 'custom'
            else:
                raise ModuleException(self.name,  "Error, use all | home | web | <file> | load:<file_list.txt> as option ")
            
        self.modhandler.load('system.users').run()
        
        for user in self.modhandler.load('system.users').usersinfo:
            
            print 'Checking user \'%s\' home \'%s\'' % (user.name, user.home)
            
            for current_mode in self.common_files:
                
                if mode == 'all' or current_mode == mode:
                    
                    for f in self.common_files[current_mode]:
                        
                        path = user.home + '/' + f
                        
                        if self.modhandler.load('file.check').run(path, 'exists', quiet=True):
                            
                            output = 'Found \'' + path + '\' '
                            
                            if self.modhandler.load('file.check').run(path, 'r', quiet=True):
                                output += 'readable '
                            if self.modhandler.load('file.check').run(path, 'w', quiet=True):
                                output += 'writable '
                            
                            print output
                            
                    
                    
        
        
            