# This file is part of Weevely NG.
#
# Copyright(c) 2011-2012 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
# http://www.backbox.org
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
from threading import Thread

class RunningException(Exception):
    pass

class ThreadPool(Thread):
    def __init__( self, window_size, prototype, async=False ):
        Thread.__init__(self)
        self.window    = window_size
        self.prototype = prototype
        self.left      = 0
        self.running   = 0
        self.active    = False
        self.pool      = []
        self.slice     = None
        self.async     = async
		
    def __str__(self):
        return "Thread Pool( Prototype={0}, Window Size={1}, Asynchronous={2}, Running={3} )".format( self.prototype, self.window, self.async, self.running )

    def pushArgs( self, *args ):
        if self.active == True:
            raise RunningException("Thread pool already running")
        else:
            self.pool.append( self.prototype(*args) )

    def run(self):
        self.__start_threads()

    def start(self):
        if self.active == True:
            raise RunningException("Thread pool already running")
    
        if self.async == True:
            super(ThreadPool,self).start()
        else:
            self.__start_threads()
        
    def stop(self):
		if self.active == False:
			raise RunningException("Thread pool is not running")
		else:
			self.active = False
			os.kill( os.getpid(), signal.SIGTERM )

    def __start_threads(self):
        self.active = True
        self.left   = len(self.pool)
        while self.left and self.active == True:
            self.slice   = self.pool[:self.window]
            self.running = 0
            
            for thread in self.slice:
				thread.start()
				self.running += 1
            for thread in self.slice:
                if self.active == False:
                    self.running = 0
                    break
                    
                thread.join()
                self.pool.remove(thread)
                self.running -= 1
            self.left -= 1

        self.active = False
