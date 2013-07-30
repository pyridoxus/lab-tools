
from instrument import gpibInstrument
from pceExceptions import InstrumentException

name = "Electronic load"


class ElectronicLoadBase(gpibInstrument):
    '''
        Electronic Load abstract base class, do not instantiate 
    '''
    
    def inputOff(self):
        raise NotImplementedError, self
        
        
    def inputOn(self):
        raise NotImplementedError, self
        
        
    def measureVoltage(self):
        raise NotImplementedError, self
        
        
    def measureCurrent(self):
        raise NotImplementedError, self
        
        
    def setCurrentMode(self, current):
        raise NotImplementedError, self
       
        
    def setResistanceMode(self, resistance):
        raise NotImplementedError, self



class EloadVirtual(ElectronicLoadBase):
    
    def __init__(self): #IGNORE:W0231 (we're not calling the parent constr)
        pass


    def inputOff(self):
        self.isInputOn = False
        
        
    def inputOn(self):
        self.isInputOn = True
        
        
    def measureVoltage(self):
        raise NotImplementedError, self
        
        
    def measureCurrent(self):
        return self.current
        
        
    def setCurrentMode(self, current):
        self.current = current
       
        
    def setResistanceMode(self, resistance):
        pass
    
    

class EloadTexio151_201(ElectronicLoadBase):
    '''
        Class for TEXIO Model 151/201 Electronic Load
    '''
    
#     def __init__(self, gpibIp, instrId):
#         ElectronicLoadBase.__init__(self, gpibIp, instrId)
#         self.target.write("EXCON 0")
#         self.target.ask("*ESR?")
#         self.target.ask("*ESR?")    # Clear ESR


    def __setup(self):
        self.target.write("EXCON 0")
        self.target.write("PRESET 0")     # #Selects "PRESET A"  
        self.target.write("REL_OCP 1")    # ...for OCP alarms
        self.target.write("REL_OPP 1")    # ...for OPP alarms
        self.target.write("SS 1")         # Sets the "soft start" time to 1 ms
    
    
    def __errorCheck(self):
        errV = self.target.ask("*ESR?")
        if errV == "*ESR 16":
            raise InstrumentException, "Nonextant command received"
        elif errV == "*ESR 32":
            raise InstrumentException, "Inexecutable command received"
                

    def inputOff(self):
        self.target.write("LOAD 0")
        self.__errorCheck()                          
        
        
    def inputOn(self):
        self.target.write("LOAD 1")
        self.__errorCheck()                          
     
        
    def measureVoltage(self):
        result = self.target.ask("VREAD?")
        self.__errorCheck()
        mcode, mresult = result.split(" ", 1)
        if mcode != "VREAD":
            raise InstrumentException, "Bad VREAD return string"
        return float(mresult)                          
    
        
    def measureCurrent(self):
        result = self.target.ask("AREAD?")
        self.__errorCheck()
        mcode, mresult = result.split(" ", 1)
        if mcode != "AREAD":
            raise InstrumentException, "Bad AREAD return string"
        return float(mresult)                          
        
        
    def setCurrentMode(self, current):
        self.inputOff()
        self.__setup()
        self.target.write("LMODE 0")       # Constant current discharge mode
        if current >= 1:                   # Currents over 1A use high range 
            self.target.write("CRNG 1")    # Set high range
        else:
            self.target.write("CRNG 0")                # Set low range
        self.target.write("CCREF 0,%f" % float(current))      # Set current
        self.target.write("UVP OFF")                   # Set UVP off
        self.target.write("OPP 1,60")                  # Set OPP to Max
        self.target.write("LOAD 1")
        self.__errorCheck()                          
   
        
    def setResistanceMode(self, resistance):
        self.inputOff()
        self.__setup()
        self.target.write("LMODE 0")     # Constant current discharge mode
        self.target.write("CRNG 0")      # Set low range
        self.target.write("LMODE 1")     # Constant resistance discharge mode
        self.target.write("CRREF 0,%d" % int(150000.0 / float(resistance)))
        self.target.write("UVP OFF")     # Set UVP off
        self.target.write("OPP 1,60")    # Set OPP to Max
        self.target.write("LOAD 1")
        self.__errorCheck()                          
