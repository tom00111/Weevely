'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module, ModuleException
from core.http.cmdrequest import CmdRequest, NoDataException
import random

classname = 'Php'
    
class Php(Module):
    '''Execute single PHP commands
    shell.sh <command;>
    '''
    
    def __init__(self, modhandler, url, password):
        Module.__init__(self, modhandler, url, password)

    def _probe(self):
        
        
        rand = str(random.randint( 11111, 99999 ))
        if self.run('echo %s;' % (rand)) != rand:
            raise ModuleException("shell.sh",  "PHP interpreter initialization failed")
        
    
    def run(self, cmd):

        
        request = CmdRequest( self.url, self.password )
        request.setPayload(cmd)
        
        try:
            resp = request.execute()
        except NoDataException, e:
            print '[-] No data returned'
        except Exception, e:
            print '[!] Error requesting data: check URL or your internet connection.'
        else:
            return resp
        

    
    
    