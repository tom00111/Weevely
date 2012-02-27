
from terminal import Terminal
from modules_handler import ModHandler
from unittest import TestCase
from terminal import help_string
from commands import getstatusoutput

class TestTerminal(Terminal):
    
    
    def run_module_cmd(self, cmd_splitted):
        
        if not self.interpreter:
            return
             
        output = ''
    
        ## Help call
        if cmd_splitted[0] == help_string:
            modname = ''
            if len(cmd_splitted)>1:
                modname = cmd_splitted[1]
            print self.modhandler.helps(modname)
            
        else:
        
            if cmd_splitted[0][0] == ':':
                interpreter = cmd_splitted[0][1:]
                cmd_splitted = cmd_splitted[1:]
            else:
                interpreter = self.interpreter
                
            output =  self.run(interpreter, cmd_splitted)
   
        if output != None:
            return output       
            
    def run_line_cmd(self, cmd_line):
        
        if not self.interpreter:
            return
             
        output = ''
        
        if cmd_line == help_string:
            print self.modhandler.helps(cmd_line[len(help_string):])
            return
        
        if not self.one_shot:

            if self._handleDirectoryChange(cmd_line) == False:
                if self.interpreter == 'shell.php' and cmd_line.startswith('ls'):
                    print self.modhandler.load('shell.php').ls_handler(cmd_line)
                    return
                
                output = self.run(self.interpreter, [ cmd_line ])  
                
            else:
                pass
            
        else:
            output = self.run(self.interpreter, [ cmd_line ])  
            
        if output != None:
            return output


class Test(TestCase):
    
    def __init__(self, modhandler):
        
        self.modhandler = modhandler
        self.terminal = TestTerminal (modhandler, True)
        
    def __run(self, cmd):

        print '\n=========== Running \'%s\'\n' % cmd
        
        if cmd[0] == ':':
            return self.terminal.run_module_cmd(cmd.split())
        else:
            return self.terminal.run_line_cmd(cmd)    
    
    def __testfail(self, cmd):
        self.assertEqual(self.__run(cmd), None, "Error: '%s'" % cmd)
    
    def runtest(self):
        
        try:
            pass
#            getstatusoutput('echo ".bashrc" > /tmp/list.txt')
#            self.__testfail(':audit.user_files list=/tmp/list.txt')
#            self.__testfail(':audit.user_files auto=web')
#            self.__testfail(':audit.user_files path=.profile')
           
#            self.__testfail(':audit.user_web_files http://disse.cting.org/~git/ /home/git/ deep=1')           
             
#             for v in self.modhandler.load('audit.users').vectors:
#                 self._assertEqual(':audit.users vector=%s' % v.name)           
                
        except KeyboardInterrupt:
            print '\n[!] Exiting. Bye ^^'