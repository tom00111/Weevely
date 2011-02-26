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
from core.terminal import Terminal

class ClusterItem(Terminal):
	def __init__( self, name, url, password ):
		Terminal.__init__( self, url, password, False, ':' )
		self.name = name

class ClusterThread(threading.Thread):
	def __init__( self, terminal, cmd, lock ):
		threading.Thread.__init__(self)
		self.terminal = terminal
		self.cmd  	  = cmd
		self.lock 	  = lock

	def run( self ):
		self.lock.acquire()
		lines = self.terminal.execute( self.cmd ).split('\n')
		if len(lines) == 1:
			print "[%s] : %s" % ( self.terminal.name, lines[0].strip() )
		else:
			print "[%s] :" % self.terminal.name
			for line in lines:		
				print "\t%s" % line.strip()		
		self.lock.release()

class ClusterTerminal:
	def __init_item( self, name, url, password ):
		self.items[ name ] = ClusterItem( name, url, password )

	def __reload( self ):
		self.items  = {}
		self.entity = "cluster"

		print "+ Initializing cluster ..."

		fd 	  	= open( self.clusterfile,'r' )
		lines 	= fd.readlines()
		i	  	= 0
		threads = []
		for line in lines:
			line = line.strip()
			if line != '' and line[0] != '#':
				items = line.split(',')
				if len(items) == 2:
					url 	 = items[0]
					password = items[1]
					name	 = "C%d" % i
				elif len(items) == 3:
					name	 = items[0]
					url 	 = items[1]
					password = items[2]
				else:
					raise Exception( "Invalid line found on cluster file :\n%s" % line )
					
				thread = threading.Thread( target = self.__init_item, args=( name, url, password, ) )
				i += 1	
				thread.start()
				threads.append(thread)

		fd.close()

		for thread in threads:	
			thread.join()

		print "+ Loaded %d items from '%s' .\n+ Type ':help' for a list of available commands.\n" % ( len(self.items), self.clusterfile )
		

	def __init__( self, clusterfile ):	
		self.clusterfile = clusterfile
		self.items 		 = {}
		self.entity      = "cluster"
		self.history 	 = os.path.expanduser( '~/.weevely_history' )
		self.completions = {}
		self.lock		 = threading.Lock()

		self.__reload()

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
				cmd = raw_input( "[%s@weevely] " % self.entity )
				cmd = cmd.strip()
				if cmd == '':
					continue
			else:
				cmd = self.items[ self.entity ].run( True )	

			if cmd[0] == ':':
				self.__parseInternalCommand(cmd)
			elif self.entity == "cluster":
				self.execute( cmd )
			
	def execute( self, cmd ):
		pool = ThreadPool( 20, ClusterThread )
		
		for name, item in self.items.items():
			pool.pushArgs( item, "cd %s && %s" % ( item.cwd, cmd ), self.lock )

		pool.start()

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
		elif cmd == 'kill':
			item_name = args[0]
			if item_name not in self.items.keys():
				print "! '%s' invalid cluster item id, allowed : %s" % ( value, ', '.join( self.items.keys() ) ),
			else:
				self.items.pop( item_name )
		elif cmd == 'list':	
			print ', '.join( self.items.keys() )
		elif cmd == 'reload':
			self.__reload()
		elif cmd == 'exit':
			print "+ Quitting application, bye ^^"
			quit()
		elif cmd == 'help':
			print "\t:switch <cluster-item> - Switch to an item terminal, type ':switch cluster' to go back."
			print "\t:kill <cluster-item>   - Remove an item from the active session given its id (see :list)."
			print "\t:list                  - Print a list of active cluster items."
			print "\t:reload                - Reload the cluster from '%s'." % self.clusterfile
			print "\t:exit					- Quit the application."
			print "\t:help                  - Print this menu."
		else:
			print "! ':%s' unknown command, type ':help' for a list of available commands." % cmd
		
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
