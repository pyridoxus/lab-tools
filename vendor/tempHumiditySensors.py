
import win32file
import win32event
import win32con
import socket
from time import sleep

from Instruments.instrument import ethernetInstrument
from Instruments.Support.pceExceptions import InstrumentException


name = "Temp/Humidity Sensor"


class TempHumiditySensorBase(ethernetInstrument):
    '''
        Temperature and Humidity Sensors abstract base class, do not instantiate 
    '''
    
    def __init__(self):
        pass


    def measureTemperature(self):
        raise NotImplementedError
        
        
    def measureHumidity(self):
        raise NotImplementedError
    


class TempHumiditySensorVirtual(TempHumiditySensorBase):
    '''
        Temperature and Humidity Sensors abstract base class, do not instantiate 
    '''
    
    def measureTemperature(self):
        return 5.0 # TODO: Set to a sensible value
        
        
    def measureHumidity(self):
        return 5.0 # TODO: Set to a sensible value
        
        

class FlukeRHT5000A(TempHumiditySensorBase):
    '''
        Class for Fluke RH/T 5000A
        
        NOTE: This class does NOT work and is NOT complete
        It is left here for historical record only. 
    '''
    
    def __init__(self, com_index):
        TempHumiditySensorBase.__init__(self)
        self.com_index = com_index
        

    def __getDataBlock(self):
        hcp = win32file.CreateFile("COM1",
               win32con.GENERIC_READ | win32con.GENERIC_WRITE,
               0, # exclusive access
               None, # no security
               win32con.OPEN_EXISTING,
               win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_OVERLAPPED,
               None)
        #
        overlappedRead = win32file.OVERLAPPED()
        overlappedRead.hEvent = win32event.CreateEvent(None, 1, 0, None)
        overlappedWrite = win32file.OVERLAPPED()
        overlappedWrite.hEvent = win32event.CreateEvent(None, 0, 0, None)
        #
        win32file.EscapeCommFunction(hcp, win32file.CLRDTR)
        sleep(1)
        win32file.EscapeCommFunction(hcp, win32file.SETDTR)
        comDCB = win32file.GetCommState(hcp)
        comDCB.BaudRate = 19200
        comDCB.ByteSize = 8
        comDCB.Parity = win32file.NOPARITY
        comDCB.fParity = 0 # Dis/Enable Parity Check
        comDCB.StopBits = win32file.ONESTOPBIT
        comDCB.fBinary = 1
        comDCB.fRtsControl = win32file.RTS_CONTROL_HANDSHAKE
        comDCB.fRtsControl = 0
        comDCB.fDtrControl = win32file.DTR_CONTROL_HANDSHAKE
        comDCB.fDtrControl = 1
        comDCB.fOutX = 1
        comDCB.fInX = 1
        comDCB.fNull = 0
        comDCB.fErrorChar = 0
        comDCB.fAbortOnError = 0
        comDCB.XonChar = chr(17)
        comDCB.XoffChar = chr(19)
        comDCB.XonLim = 100
        comDCB.XoffLim = 100
        win32file.SetCommState(hcp, comDCB)
        win32file.SetupComm(hcp, 1000, 1000)
        win32file.PurgeComm(hcp, 
                            win32file.PURGE_TXCLEAR | win32file.PURGE_TXABORT | 
                            win32file.PURGE_RXCLEAR | win32file.PURGE_RXABORT)
        win32file.SetCommTimeouts(hcp, (0, 0, 0, 0, 504))
        _err, n = win32file.WriteFile(hcp, "\x01\x49\x00\x00\x00\x00\x49\xB6", 
                                      overlappedWrite)
        win32file.EscapeCommFunction(hcp, win32file.SETRTS)
        win32file.SetCommTimeouts(hcp, (0, 0, 500, 0, 0))
        # read
        _rc, buf = win32file.ReadFile(hcp, win32file.AllocateReadBuffer(1024), 
                                      overlappedRead)
        n = win32file.GetOverlappedResult(hcp, overlappedRead, 1)
        read_buffer1 = str(buf[:n])
        win32file.SetCommTimeouts(hcp, (0, 0, 924, 0, 0))
        # read
        _rc, buf = win32file.ReadFile(hcp, win32file.AllocateReadBuffer(1024), 
                                      overlappedRead)
        n = win32file.GetOverlappedResult(hcp, overlappedRead, 1)
        read_buffer2 = str(buf[:n])
        win32file.EscapeCommFunction(hcp, win32file.CLRRTS)
        win32file.EscapeCommFunction(hcp, win32file.CLRDTR)
        win32file.CloseHandle(hcp)
        return read_buffer1 + read_buffer2
        
        
    def measureTemperature(self):
        _data_block = self.__getDataBlock()
        # parse out the temperature and humidity
        # return temperature
        
        
    def measureHumidity(self):
        _data_block = self.__getDataBlock()
        # parse out the temperature and humidity
        # return temperature
    
    
    
class OmegaMicroserver(TempHumiditySensorBase):
    '''
        Class for Omega iTHX-W Microserver
        
    '''
    
    def __init__(self, ip_address):
        TempHumiditySensorBase.__init__(self)
        self.ip_address = ip_address
        

    def __sendMicroserverCommand(self, textcmd):
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((self.ip_address, 1000))
        proxy_socket.send("*%s\r" % textcmd)
        response = proxy_socket.recv(6)
        proxy_socket.close()
        return response


    def __commandRetryWrapper(self, textcmd):
        retries = 0
        while(1):
            try:
                response = self.__sendMicroserverCommand(textcmd)
            except:
                msg = "Temperature/Humidity Sensor not responding."
                raise InstrumentException(msg)
            if response != "":
                return response
            retries = retries + 1
            if retries == 10:
                msg = "Temperature/Humidity Sensor communication error."
                raise InstrumentException(msg)


    def measureTemperature(self):
        return float(self.__commandRetryWrapper("SRTC"))
    
        
    def measureHumidity(self):
        return float(self.__commandRetryWrapper("SRH"))


if __name__ == "__main__":
    
    sensor = OmegaMicroserver("192.168.0.106")
