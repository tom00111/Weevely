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
import readline, rlcompleter, atexit, urlparse, os, re
from core.shell import Shell

class Terminal(Shell):
	def __init__( self, url, password ):
		Shell.__init__( self, url, password )
		print "+ Retrieving terminal basic environment variables .\n"
		self.username 	 = self.execute("whoami")
		self.hostname 	 = self.execute("hostname")
		self.cwd		 = self.execute("pwd")
		self.prompt   	 = "[%s@%s %s] " % (self.username, self.hostname, self.cwd)
		self.history 	 = os.path.expanduser( '~/.weevely_history' )
		self.completions = {}

		self.cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )

		try:
			readline.parse_and_bind( 'tab: menu-complete' )
			readline.set_completer( self.__complete )
			readline.read_history_file( self.history )
		except IOError:
			pass

		atexit.register( readline.write_history_file, self.history )

	def run( self ):
		while True:
			self.prompt = "[%s@%s %s] " % (self.username, self.hostname, self.cwd)
			cmd 		= raw_input( self.prompt )
			if cmd != '\n':
				cmd = cmd.strip()
				cd  = self.cwd_extract.findall(cmd)

				if cd != None and len(cd) > 0:	
					cwd = cd[0].strip()
					if cwd[0] == '/':
						self.cwd = cwd
					elif cwd == '..':
						dirs = self.cwd.split('/')
						dirs.pop()
						self.cwd = '/'.join(dirs)
					elif cwd == '.':
						pass
					elif cwd[0:3] == '../':
						self.cwd = cwd.replace( '../', self.cwd )
					elif cwd[0:2] == './':
						self.cwd = cwd.replace( './', self.cwd )
					else:
						self.cwd = (self.cwd + "/" + cwd).replace( '//', '/' ) 
				else:
					readline.add_history(cmd)

					cmd = "cd %s && %s" % ( self.cwd, cmd )					
					print self.execute(cmd)

	def __complete( self, text, state ):
		try:
			matches = self.completions[text]
		except KeyError:
			matches = []
			items   = readline.get_current_history_length()
			for i in range( items ):
				item = readline.get_history_item(i)
				if item != None and text in item:
					matches.append(item)
		
			self.completions[text] = matches
		
		try:
			return matches[state]
		except IndexError:
			return None

