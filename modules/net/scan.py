'''
Created on 20/set/2011

@author: norby
'''


from core.module import Module, ModuleException
from core.vector import VectorList, Vector as V
from core.parameters import ParametersList, Parameter as P

from external.ipaddr import IPNetwork, IPAddress, summarize_address_range

classname = 'Scan'
    
    
class RequestList:
    
    def __init__(self, modhandler):
        
        self.modhandler = modhandler
        
        self.ips = []
        self.ports = []
        self.ifaces = {}
        
    def networks_add(self, net):
        
        
        if ',' in net:
            addresses = net.split(',')
        else:
            addresses = [ net ]    
        
        for addr in addresses:
            self.__set_networks(addr)
        
    def ports_add(self, port):
        
        if ',' in port:
            port_ranges = port.split(',')
        else:
            port_ranges = [ port ]    
        
        for ports in port_ranges:
            self.__set_port_ranges(ports)

    def __set_port_ranges(self, given_range):

            start_port = None
            end_port = None
            

            if given_range.count('-') == 1:
                try:
                    splitted_ports = [ int(strport) for strport in given_range.split('-') if (int(strport) > 0 and int(strport) <= 65535)]
                except ValueError:
                    return None
                else:
                    if len(splitted_ports) == 2:
                        start_port = splitted_ports[0]
                        end_port = splitted_ports[1]
                        
            else:
                try:
                    int_port = int(given_range)
                except ValueError:
                    return None   
                else:
                    start_port = int_port
                    end_port = int_port
                    
            self.ports.append((start_port, end_port))
                    

    def __get_network_from_ifaces(self, iface):
        
        if not self.ifaces:
            
            self.modhandler.set_verbosity(6)
            self.modhandler.load('net.ifaces').run()
            self.modhandler.set_verbosity()
            
            self.ifaces = self.modhandler.load('net.ifaces').ifaces
            
        
        if iface in self.ifaces.keys():
             return self.ifaces[iface]
                       
            


    def __set_networks(self, addr):
        
        
        networks = []
        
        try:
            # Parse single IP or networks
            networks.append(IPNetwork(addr))
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
            else:
                
                # Parse interface name
                remote_iface = self.__get_network_from_ifaces(addr)
                if remote_iface:
                    networks.append(remote_iface)  

        if not networks:       
            print '[net.scan] Warning: \'%s\' is not an IP address, network or detected interaface' % ( addr)
            
        else:
            for net in networks:
                self.ips += [ str(ip) for ip in net ]
                

    
    
class Scan(Module):

    params = ParametersList('Scan network for open ports', [],
                    P(arg='addr', help='IP address, multiple addresses (IP1,IP2,..), networks (IP/MASK or IPstart-IPend) or interfaces (eth0)', required=True, pos=0),
                    P(arg='port', help='Port or multiple ports (PORT1, PORT2,.. or startPORT-endPORT)', required=True, pos=1))
    


    def __init__(self, modhandler, url, password):
        self.reqlist = RequestList(modhandler)
        
        Module.__init__(self, modhandler, url, password)    

    
    def run_module(self, addr, port):
        
        self.reqlist.networks_add(addr)
        self.reqlist.ports_add(port)
        
        print self.reqlist.ips
        print self.reqlist.ports
