
from terminal import Terminal
from modules_handler import ModHandler

class Test:
    
    commands = [
                
                ":audit.user_files .profile",
                "mkdir asd/prova",
                "chmod 777 asd/prova",
                ":file.upload /etc/passwd ./asd/prova/test",
                ":file.check asd/prova/test exists",
                "rm asd/prova/test",
                ":file.check asd/prova/test r",
                #":audit.user_web_files /var/www http://site.org/",
                ":audit.users",
                ":enum.binaries telnet",
                ":enum.paths /home/asd/",
                 ":sql.query mysql localhost asd asdasd 'SHOW databases;'",
                 ":sql.summary mysql localhost asd asdasd asd"
                ]
    
    def run(self, url, password):
        
        for cmd in self.commands:
               
            print '\n=========== Running \'%s\' test\n' % cmd
               
            try:
                
                terminal = Terminal (ModHandler(url, password), True)
                if cmd[0] == terminal.module_char:
                    terminal.run_module_cmd(cmd.split())
                else:
                    terminal.run_line_cmd(cmd)
                    
            except KeyboardInterrupt:
                print '\n[!] Exiting. Bye ^^'