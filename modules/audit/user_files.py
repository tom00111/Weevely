

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P


classname = 'UserFiles'

class UserFiles(Module):
    """Enumerate common restricted files in home and public_html folders"""
    
    params = ParametersList('Enumerate common restricted files for every system user', [],
                    P(arg='auto', help='Specify home for \'/home/*\', web for \'/home/*/public_html\', any for both', choices = ['home', 'web', 'any']),
                    P(arg='list', help='Path list from local file', mutual_exclusion=['auto', 'path']),
                    P(arg='path', help='Single path', mutual_exclusion=['list', 'auto'])
                    )
    
    common_files = { 
                    
                    "home" : [ ".bashrc", 
                              ".bash_history", 
                              ".profile",
                              ".ssh",
                              ".ssh/authorized_keys",
                              ".ssh/known_hosts"
                              ],
                    "web" : [ "public_html/", 
                             "public_html/wp-config.php", # wordpress
                             "public_html/config.php", 
                             "public_html/uploads",
                             "public_html/configuration.php", # joomla
                             "public_html/sites/default/settings.php", # drupal
                             "public_html/.htaccess" ] 
                    
                    }

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run_module(self, auto, list, path):
 
        custom_files = []
        
        if list != None:
            try:
                custom_files=open(list,'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % list)
        
        elif path != None:
            custom_files = path.split(',')
            
        elif auto:
            if auto == 'any':
                custom_files = self.common_files['home'] + self.common_files['web']
            else:
                custom_files = self.common_files[auto]
                
        else:
            print '[!] Error, required one of this parameters: %s' % (self.params.summary())
            return
        
        self.modhandler.set_verbosity(2)
        self.modhandler.load('audit.etc_passwd').run({'filter' : 'True'})
        self.modhandler.set_verbosity()
        
        
        path_list = []
        user_dict = self.modhandler.load('audit.etc_passwd').usersinfo
            
        self.mprint('[%s] Enumerating %i users' % (self.name, len(user_dict.keys())))
        
        for username in user_dict:
            for f in custom_files:
                path_list.append(user_dict[username].home + '/' + f)
                     
        if path_list:
            
            self.modhandler.load('file.enum').set_list(path_list)
            self.modhandler.load('file.enum').run({'lpath' : ''})
        
            