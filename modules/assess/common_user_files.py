

from core.module import Module, ModuleException

classname = 'CommonUserFiles'

class CommonUserFiles(Module):
    """Enumerate common user file in home or public_html folders
    :assessment.common_user_files all | home | web
    """
    
    
    common_files = { 
                    
                    "home" : [ ".bashrc", 
                              ".bash_history", 
                              ".profile"],
                    "web" : [ "/public_html/", 
                             "/public_html/wp-config.php", 
                             "/public_html/config.php", 
                             "/public_html/uploads",
                             "/public_html/.htaccess" ] 
                    
                    }

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run(self, mode):
        
        if mode != 'all' and mode not in self.common_files.keys():
            raise ModuleException(self.name,  "Error, use all|home|web as option ")
            
        self.modhandler.load('system.users').run()
        
        for user in self.modhandler.load('system.users').usersinfo.keys():
            
            if user:
                print 'User:', user
                
                for current_mode in self.common_files:
                    if current_mode == 'all' or current_mode == mode:
                        
                        for file in self.common_files[current_mode]:
                            
                            path = '/home/' + user + file
                            
                            if self.modhandler.load('file.check').run(path, 'exists', quiet=True):
                                
                                output = 'File \'' + path + '\' '
                                
                                if self.modhandler.load('file.check').run(path, 'r', quiet=True):
                                    output += 'readable '
                                if self.modhandler.load('file.check').run(path, 'w', quiet=True):
                                    output += 'writable '
                                
                                print output
                                
                        
                        
            
            
            