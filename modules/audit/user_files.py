

from core.module import Module, ModuleException

classname = 'UserFiles'

class UserFiles(Module):
    """Enumerate common files in home and public_html folders
    :enum.user_files auto | home | web | <file path> | load:<path_list.txt>
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
        
        if mode != 'auto' and mode not in self.common_files.keys():
            
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
                raise ModuleException(self.name,  "Error, use auto | home | web | <file path> | load:<path_list.txt> as option ")
            
        self.modhandler.set_verbosity(1)
        self.modhandler.load('audit.users').run()
        self.modhandler.set_verbosity()
        
        
        path_list = []
        user_list = self.modhandler.load('audit.users').usersinfo
            
        self.mprint('[%s] Enumerating %i users' % (self.name, len(user_list)))
        
        for user in user_list:
            for current_mode in self.common_files:
                if mode == 'auto' or current_mode == mode:
                    for f in self.common_files[current_mode]:
                        path_list.append(user.home + '/' + f)
                     
        
        if path_list:
            self.modhandler.load('enum.paths').run('', path_list)
                    
                       
                            
                    
                    
        
        
            