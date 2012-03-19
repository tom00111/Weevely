'''
Created on 03/ott/2011

@author: emilio
'''

import urllib
from random import randint

agents = ( 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6', \
           'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14', \
           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; InfoPath.1)' )

class URLOpener(urllib.FancyURLopener):
    
    version = agents[ randint( 0, len(agents) - 1 ) ]
    
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass
    
    
class Request:
    
    def __init__(self, url, proxy={}):
        self.url = url
        self.data = {}
        
        self.opener = URLOpener(proxies = proxy)
        
    def __setitem__(self, key, value):
        self.opener.addheader(key, value)
        
    def read(self, bytes= -1):
        if self.data:
            handle = self.opener.open(self.url, data=urllib.urlencode(self.data))
        else:
            handle = self.opener.open(self.url)
            
        if bytes > 0: 
            return handle.read(bytes)
        else:
            return handle.read()