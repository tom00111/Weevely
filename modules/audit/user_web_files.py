

from core.module import Module, ModuleException
from external.crawler import Crawler

classname = 'UserWebFiles'

class UserWebFiles(Module):
    """Enumerate w/r/x files in web folders
    :audit.user_web_files /home/user/public_html/ http://www.site.com/user/
    """
    
    

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run(self, home, url, depth_limit = 3):
        
        depth_limit = 5
        confine_prefix = url
        exclude = ''

        if home[-1] != '/': home = home + '/'

        self.mprint('[%s] Crawling paths in %s (depth %i)' % (self.name, url, depth_limit))
        
        try:
            crawler = Crawler(url, depth_limit, confine_prefix, exclude)
            crawler.crawl()
        except Exception, e:
            raise ModuleException(self.name, "Crawler exception: %s" % str(e))
        
        path_list = [ home + p[len(url):] for p in crawler.urls_remembered ]
            
        self.mprint('[%s] Enumerating %i paths in %s' % (self.name, len(path_list), home))

        if path_list:
            self.modhandler.load('enum.paths').run('', path_list)
                    
                       
                            
                    
                    
        
        
            