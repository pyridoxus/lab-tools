
from time import sleep

from instrument import gpibInstrument        
from pceExceptions import InstrumentException

name = "Power supply"

class PowerSupplyBase(gpibInstrument):
    '''
        power supply abstract base class, do not instantiate 
    '''
    
    def inputOff(self):
        raise NotImplementedError, self
        
        
    def setVoltage(self, voltage, current_limit):
        raise NotImplementedError, self
    
    
    def measureCurrent(self):
        raise NotImplementedError, self


    def isOverCurrent(self):
        raise NotImplementedError, self


    def isOverVoltage(self):
        raise NotImplementedError, self



class PowerSupplyVirtual(PowerSupplyBase):
    
    def __init__(self): #IGNORE:W0231 (we're not calling the parent constr)
        pass 


    def inputOff(self):
        pass
        
        
    def setVoltage(self, voltage, current_limit, overCurrentLimit):
        pass
    
    
    def measureCurrent(self):
        return 0.05 # TODO: Return a sensible value
    
    
    def isOverCurrent(self):
        return False


    def isOverVoltage(self):
        return False


    
class PowerSupplyInstekPsm6003(PowerSupplyBase):
    '''
        Class for Gw INSTEK PSM-6003 Power Supply
    ''' 
    #
    # Implementation Note:
    # This power supply does NOT implement the :CURRent:PROTection:DELay
    # command as described in its programming manual.
    # Because of this the overcurrent protection mechanism trips
    # very easily so set the overcurrent limit VERY high.
    #
    
    def __clearTrippedCurrentProtection(self):
        if self.target.ask(":CURRent:PROTection:TRIPped?") == "1":
            self.target.write(":CURRent:PROTection:CLEar")


    def __clearTrippedVoltageProtection(self):
        if self.target.ask(":VOLTage:PROTection:TRIPped?") == "1":
            self.target.write(":VOLTage:PROTection:CLEar")


    def __errorCheck(self):
        '''
        This will poll the error queue until it is empty 
        and raises an exception if anything was in the queue
        '''
        errV = self.target.ask(":SYSTem:ERRor?")
        raiseMsg = ""
        while(errV[0] != '0'):
            raiseMsg = errV
            errV = self.target.ask(":SYSTem:ERRor?")
        if raiseMsg != "":            
            raise InstrumentException, raiseMsg              
        return
    
    
    def inputOff(self):
        '''
        Turns off the power supply.
        '''
        self.__clearTrippedCurrentProtection()        
        self.__clearTrippedVoltageProtection()        
        self.target.write(":OUTPut:STATe 0")
        self.__errorCheck()                                                   
        
        
    def setVoltage(self, voltage, current_limit, over_current_protection): 
        '''
        Sets the voltage, the voltage range, and the current limit.
        '''
        self.__clearTrippedCurrentProtection()        
        self.__clearTrippedVoltageProtection()        
        self.target.write(":VOLTage:PROTection:STATe OFF")
        self.target.write(":CURRent:PROTection:STATe OFF")
        if voltage > 30:
            self.target.write(":VOLTage:RANGe P60V")
        else:
            self.target.write(":VOLTage:RANGe P30V")
        self.target.write(":CURRent:PROTection %f" % current_limit)
        self.target.write(":CURRent %s" % over_current_protection)
        self.target.write(":VOLTage %f" % voltage)
        self.target.write(":OUTPut:STATe 1")
        sleep(3.0)
        self.target.write(":CURRent:PROTection:STATe ON")
        self.__errorCheck()                          
     
            
    def measureCurrent(self):
        '''
        Measures the current being put out by the power supply
        '''
        result = self.target.ask(":MEASure:CURRent?")
        self.__errorCheck()
        return float(result)


    def isOverCurrent(self):
        if self.target.ask(":CURRent:PROTection:TRIPped?") == "1":
            return True
        return False


    def isOverVoltage(self):
        if self.target.ask(":VOLTage:PROTection:TRIPped?") == "1":
            return True
        return False