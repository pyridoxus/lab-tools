
from telnetlib import Telnet

class DigiPortException(Exception):
    
    pass



class DigiPortServer:
    
    def __init__(self, ip):
        self.ip = ip 
        self.userName = "root"
        self.password = "dbps"
        
        
    def createNewConn(self):
        '''
        Connects to a digiport device and logs in
        '''
        portObj = Telnet(self.ip)
        portObj.read_until("login: ")
        portObj.write(self.userName + "\n")
        portObj.write(self.password + "\n")  
        return portObj
    
    
    def killConnection(self, tty=4, timeout=0.1):
        '''
        Kills a connection on the teststand digiport
        '''
        portObj = self.createNewConn()     
        portObj.write("kill %d\n" % tty)
        portObj.read_until("blah", timeout)
        portObj.close()


    def closeConnection(self, tty):
        '''
        Closes a connection on the teststand digiport
        '''
        portObj = self.createNewConn()     
        portObj.write("close %d\n" % tty)
        portObj.read_until("blah", 5)
        portObj.close()
                
        
        
digiPort = DigiPortServer("172.24.24.20")#"192.168.0.139")
