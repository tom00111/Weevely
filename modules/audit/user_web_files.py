

from core.module import Module, ModuleException
from core.parameters import ParametersList, Parameter as P
from external.crawler import Crawler

classname = 'UserWebFiles'

class UserWebFiles(Module):
    """Enumerate w/r/x files in web folders
    :audit.user_web_files http://www.site.com/user/ /home/user/public_html/ 
    """
    params = ParametersList('First crawl web site, then enumerate files searching w/r/x permissions', None,
            P(arg='url', help='Site to crawl', required=True, pos=0),
            P(arg='rpath', help='Remote root path corresponding to crawled site', required=True, pos=1),
            P(arg='deep', help='Crawl deepness', default=3, type=int, pos=2),
            )

    def __init__( self, modhandler , url, password):

        Module.__init__(self, modhandler, url, password)
        
        self.usersfiles = {}    
        
        
    def run_module(self, url, home, depth_limit):
        
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
            self.modhandler.load('file.enum').set_list(path_list)
            self.modhandler.load('file.enum').run({'lpath' : ''})
                    
                       
                            
                    
                    
        
        
            