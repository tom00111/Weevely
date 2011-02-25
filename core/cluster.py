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
import readline, rlcompleter, atexit, urlparse, os, re, urlparse, threading
from core.shell import Shell
from core.threadpool import ThreadPool

class ClusterItem(Shell):
	def __init__( self, name, url, password ):
		Shell.__init__( self, url, password )
		self.name 		 = name
		self.username 	 = self.execute("whoami")
		self.hostname 	 = self.execute("hostname")
		self.cwd		 = self.execute("pwd")
		
	def prompt( self ):
		return "[%s@%s %s] " % (self.username, self.hostname, self.cwd)

class ClusterThread(threading.Thread):
	def __init__( self, item, cmd, lock ):
		threading.Thread.__init__(self)
		self.item = item
		self.cmd  = cmd
		self.lock = lock

	def run( self ):
		self.lock.acquire()
		lines = self.item.execute( self.cmd ).split('\n')
		if len(lines) == 1:
			print "[%s] : %s" % ( self.item.name, lines[0].strip() )
		else:
			print "[%s] :" % self.item.name
			for line in lines:		
				print "\t%s" % line.strip()		
		self.lock.release()

class ClusterTerminal:
	def __init_item( self, i, url, password ):
		self.items[ "C%d" % i ] = ClusterItem( "C%d" % i, url, password )

	def __init__( self, clusterfile ):	
		self.clusterfile = clusterfile
		self.items 		 = {}
		self.entity      = "cluster"
		self.prompt   	 = "[%s@weevely] " % self.entity
		self.history 	 = os.path.expanduser( '~/.weevely_history' )
		self.completions = {}
		self.lock		 = threading.Lock()
		self.cwd_extract = re.compile( "cd\s+(.+)", re.DOTALL )

		print "+ Initializing cluster ..."

		fd 	  	= open( clusterfile,'r' )
		lines 	= fd.readlines()
		i	  	= 0
		threads = []
		for line in lines:
			line = line.strip()
			if line != '' and line[0] != '#':
				url , password = line.split(',')
				thread = threading.Thread( target = self. __init_item, args=( i, url, password, ) )
				i += 1	
				thread.start()
				threads.append(thread)

		fd.close()

		for thread in threads:
			thread.join()

		print "+ Loaded %d items from '%s' .\n+ Type ':help' for a list of available commands.\n" % ( len(self.items), self.clusterfile )

		try:
			readline.parse_and_bind( 'tab: menu-complete' )
			readline.set_completer( self.__complete )
			readline.read_history_file( self.history )
		except IOError:
			pass

		atexit.register( readline.write_history_file, self.history )

	def run( self ):
		while True:
			if self.entity == "cluster":
				self.prompt = "[%s@weevely] " % self.entity
			else:
				self.prompt = self.items[ self.entity ].prompt()

			cmd = raw_input( self.prompt ).strip()
			if cmd == '':
				continue

			if cmd[0] == ':':
				self.__parseInternalCommand(cmd)
			elif self.entity == "cluster":
				pool = ThreadPool( 20, ClusterThread )
				
				for name, item in self.items.items():
					pool.pushArgs( item, "cd %s && %s" % ( item.cwd, cmd ), self.lock )

				pool.start()
			else:
				item = self.items[ self.entity ]
				if self.__handleDirectoryChange( item, cmd ) == False:
					print item.execute( "cd %s && %s" % ( item.cwd, cmd ) )				

			readline.add_history(cmd)

	def __parseInternalCommand( self, cmd ):	
		cmd   = cmd[1:]
		items = cmd.split( ' ' )
		cmd	  = items[0]
		args  = items[1:]
		
		if cmd == 'switch' and len(args) == 1:
			item_name = args[0]
			if item_name not in self.items.keys() and item_name != 'cluster':
				print "! '%s' invalid cluster item id, allowed : cluster, %s" % ( value, ', '.join( self.items.keys() ) ),
			else:
				self.entity = item_name
		elif cmd == 'list':	
			print ', '.join( self.items.keys() )
		elif cmd == 'help':
			print "\t:switch <cluster-item> - Switch to an item terminal, type ':switch cluster' to go back."
			print "\t:list                  - Print a list of active cluster items."
			print "\t:help                  - Print this menu."
		
	def __handleDirectoryChange( self, item, cmd ):
		cd  = self.cwd_extract.findall(cmd)
		if cd != None and len(cd) > 0:	
			cwd = cd[0].strip()
			if cwd[0] == '/':
				item.cwd = cwd
			elif cwd == '..':
				dirs = item.cwd.split('/')
				dirs.pop()
				item.cwd = '/'.join(dirs)
			elif cwd == '.':
				pass
			elif cwd[0:3] == '../':
				item.cwd = cwd.replace( '../', item.cwd )
			elif cwd[0:2] == './':
				item.cwd = cwd.replace( './', item.cwd )
			else:
				item.cwd = (item.cwd + "/" + cwd).replace( '//', '/' ) 
			
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
