
from terminal import Terminal
from modules_handler import ModHandler

class Test:
    
    commands = [
                
                ":audit.user_files .profile",
                ":file.upload /etc/passwd asd/test",
                ":file.check asd/test exists",
                "rm asd/test",
                ":file.check asd/test r",
#                ":audit.user_web_files /var/www http://localhost/",
                ":audit.users",
                ":enum.binaries telnet",
#                ":enum.paths /home/norby/prov",
                 ":system.info auto",
                 ":sql.query mysql localhost emilio 1101995 'SHOW TABLES FROM emilio;'"
                
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