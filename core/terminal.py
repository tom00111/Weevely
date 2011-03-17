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
	def __init__( self, url, password, verbose_init = True, ignore_char = None ):
		Shell.__init__( self, url, password )
		if verbose_init == True:
			print "+ Retrieving terminal basic environment variables .\n"

		self.username 	 = self.execute("whoami")
		self.hostname 	 = self.execute("hostname")
		self.cwd		 = self.execute("pwd")
		self.ignore_char = ignore_char
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

	def run( self, once = False ):
		while True:
			self.prompt = "%s@%s:%s$ " % (self.username, self.hostname, self.cwd)
			cmd 		= raw_input( self.prompt )
			cmd			= cmd.strip()
			if cmd != '':
				if not (self.ignore_char != None and cmd[0] == self.ignore_char):
					if self.__handleDirectoryChange(cmd) == False:
						readline.add_history(cmd)

					cmd = "cd %s && %s" % ( self.cwd, cmd )					
					print self.execute(cmd)
			
			if once == True:
				return cmd

	def __handleDirectoryChange( self, cmd ):
		cd  = self.cwd_extract.findall(cmd)
		if cd != None and len(cd) > 0:	
			cwd  = cd[0].strip()
			path = self.cwd
			if cwd[0] == '/':
				path = cwd
			elif cwd == '..':
				dirs = path.split('/')
				dirs.pop()
				path = '/'.join(dirs)
			elif cwd == '.':
				pass
			elif cwd[0:3] == '../':
				path = cwd.replace( '../', path )
			elif cwd[0:2] == './':
				path = cwd.replace( './', path )
			else:
				path = (path + "/" + cwd).replace( '//', '/' ) 
			
			exists = self.execute( "( [[ -d '%s' ]] && echo 1 ) || echo 0" % path )
			if exists == "1":
				self.cwd = path
			else:
				print "! The directory '%s' does not exist or is not accessible." % path

			return True

		return False

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

