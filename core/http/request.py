# This file is part of Weevely NG.
#
# Copyright(c) 2011-2012 Weevely Developers
# http://code.google.com/p/weevely/
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import urllib

class URLOpener(urllib.FancyURLopener):
    def http_error_206( self, url, fp, errcode, errmsg, headers, data = None ):
        pass

class Request:
	def __init__( self, url ):
		self.url	= url
		self.opener = URLOpener()

	def __setitem__( self, key, value ):
		self.opener.addheader( key, value )

	def read( self, bytes = -1 ):
		handle = self.opener.open(self.url)
		if bytes > 0: 
			return handle.read(bytes)
		else:
			return handle.read()
