'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

from external.ipaddr import IPNetwork, IPAddress, summarize_address_range

classname = 'Scan'
    
class Scan(Module):

    params = ParametersList('Scan network for open ports', [],
                    P(arg='addr', help='IP address, multiple addresses (IP1,IP2,..), networks (IP/MASK or IPstart-IPend) or interfaces (eth0)', required=True, pos=0),
                    P(arg='port', help='Port or multiple ports (PORT1, PORT2,.. or startPORT-endPORT)', required=True, pos=1))
    

    def __get_port_range(self, given_range):


            if given_range.count('-') == 1:
                try:
                    splitted_ports = [ int(strport) for strport in given_range.split('-')]
                except ValueError:
                    return None
                else:
                    for prt in splitted_ports:
                        if prt > 0 and prt < 65535:
                            return given_range
                        
            else:
                try:
                    int(given_range)
                except ValueError:
                    return None   
                else:
                    return '%s-%s' % (given_range, given_range) 
                             




    def __format_ports(self, given_port):
        
        ports = []

        if ',' in given_port:
            port_ranges = given_port.split(',')
        else:
            port_ranges = [ given_port ]    


        for p in port_ranges:
            port_range = self.__get_port_range(p)
            
            
            if port_range:
                ports.append(port_range)
            else:  
                self.mprint('[%s] Warning: \'%s\' is not a port range' % (self.name, p))
                  
                
        return ports
                
                    

    def __format_address(self, given_addr):
        
        
        networks = []
        
        if ',' in given_addr:
            addresses = given_addr.split(',')
        else:
            addresses = [ given_addr ]    


        for addr in addresses:
            
            try:
                # Parse single IP or networks
                networks.append(IPNetwork(addr))
                continue
            except ValueError:
                
                #Parse IP-IP
                if addr.count('-') == 1:
                    splitted_addr = addr.split('-')
                    # Only adress supported
                    
                    try:
                        start_address = IPAddress(splitted_addr[0])
                        end_address = IPAddress(splitted_addr[1])
                    except ValueError:
                        pass
                    else:
                        networks += summarize_address_range(start_address, end_address)
                        continue
                else:
                    
                    # Parse interface name
                    
                    self.modhandler.set_verbosity(6)
                    self.modhandler.load('net.ifaces').run()
                    self.modhandler.set_verbosity()
                    
                    remote_ifaces = self.modhandler.load('net.ifaces').ifaces
                    if addr in remote_ifaces:
                        networks.append(remote_ifaces[addr])
                        continue
                    
            self.mprint('[%s] Warning: \'%s\' is not an IP address, network or detected interaface' % (self.name, addr))
                        
        return networks
                
                
            
            

    
    def run_module(self, addr, port):
        
        print self.__format_address(addr)
        print self.__format_ports(port)
