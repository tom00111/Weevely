

from core.module import Module, ModuleException

classname = 'CommonUserFiles'

class CommonUserFiles(Module):
    """Enumerate common user file in home or public_html folders
    :assess.common_user_files all | home | web
    """
    
    
    common_files = { 
                    
                    "home" : [ ".bashrc", 
                              ".bash_history", 
                              ".profile"],
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
            raise ModuleException(self.name,  "Error, use all|home|web as option ")
            
        self.modhandler.load('system.users').run()
        
        for user in self.modhandler.load('system.users').usersinfo:
            
            print 'Checking user \'%s\' home \'%s\'' % (user.name, user.home)
            
            for current_mode in self.common_files:
                
                if mode == 'all' or current_mode == mode:
                    
                    for f in self.common_files[current_mode]:
                        
                        path = user.home + '/' + f
                        
                        if self.modhandler.load('file.check').run(path, 'exists', quiet=True):
                            
                            output = 'File \'' + path + '\' '
                            
                            if self.modhandler.load('file.check').run(path, 'r', quiet=True):
                                output += 'readable '
                            if self.modhandler.load('file.check').run(path, 'w', quiet=True):
                                output += 'writable '
                            
                            print output
                            
                    
                    
        
        
            