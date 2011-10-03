'''
Created on 03/ott/2011

@author: emilio
'''

import urllib

class URLOpener(urllib.FancyURLopener):
    
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