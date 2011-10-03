import urllib

class URLOpener(urllib.FancyURLopener):
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass

class Request:
	def __init__(self, url, proxy = {}):
		self.url	 = url
		self.opener = URLOpener(proxies = proxy)

	def __setitem__(self, key, value):
		self.opener.addheader(key, value)

	def read(self, bytes= -1):
		handle = self.opener.open(self.url, data=self.data)
		if bytes > 0: 
			return handle.read(bytes)
		else:
			return handle.read()

