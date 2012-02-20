

from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P


classname = 'UserFiles'

class UserFiles(Module):
    """Enumerate common restricted files in home and public_html folders
    :audit.user_files auto | home | web | <remote path> | load:<local_path_list.txt>
    """
    
    params = ParametersList('Enumerate common restricted files for every system user', [],
                    P(arg='common', help='Enumerate file in /home/*, /home/*/public_html or both', choices = ['home', 'web', 'any'], mutual_exclusion = ['list', 'path']),
                    P(arg='list', help='Path list from local file', mutual_exclusion = ['common', 'path']),
                    P(arg='path', help='Single path', mutual_exclusion = ['common', 'list'])
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
                             "public_html/wp-config.php", 
                             "public_html/config.php", 
                             "public_html/uploads",
                             "public_html/.htaccess" ] 
                    
                    }

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run_module(self, mode):
        
        custom_files = []
        
        listval =  self.params.get_parameter_value('list')
        if listval:
            try:
                custom_files=open(listpar.value,'r').read().splitlines()
            except:
                raise ModuleException(self.name,  "Error opening path list \'%s\'" % listpar.value)
        
        pathval =  self.params.get_parameter_value('list')
        if pathval:
            custom_files = mode.split(',')
            
        autoval = self.params.get_parameter_value('auto')
        if autoval:
            if autoval == 'any':
                custom_files = self.common_files['home'] + self.common_files['web']
            else:
                custom_files = self.common_files[autoval]
        
        self.modhandler.set_verbosity(1)
        self.modhandler.load('audit.users').run()
        self.modhandler.set_verbosity()
        
        
        path_list = []
        user_list = self.modhandler.load('audit.users').usersinfo
            
        self.mprint('[%s] Enumerating %i users' % (self.name, len(user_list)))
        
        for user in user_list:
            for f in custom_files:
                path_list.append(user.home + '/' + f)
                     
        if path_list:
            self.modhandler.load('enum.paths').run('', path_list)
                    
                       
                            
                    
                    
        
        
            