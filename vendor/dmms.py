
import random

from instrument import gpibInstrument
from Instruments.Support import connInterface
from Instruments.Support import pceExceptions
name = "DMM"

def modeCheck(func):
    '''
    A decorator that provides a speed optimization
    
    Changing the current mode is expensive--so only
        change if we have to.
    '''
    
    def wrappedMode(self, *args):
        '''
        This prevents us from having to change
        the mode if its already been set.
        '''
        if self.verifyMode(func.func_name):
            return # No need to change modes
        self.currentMode = func.func_name
        return func(self, *args)
    
    return wrappedMode



class DmmBase(gpibInstrument):
    '''
        dmm abstract base class, do not instantiate 
    '''
    
    currentMode = None
    
    def __init__(self, gpibIp, instrId):
        self.target = connInterface.connectToInstrumentOverGpib(gpibIp, instrId)
        

    def setDcVoltsMode(self):
        raise NotImplementedError, self
   
        
    def setAcVoltsMode(self):
        raise NotImplementedError, self
  
        
    def setDcCurrentMode(self):
        raise NotImplementedError, self
    
        
    def set2WireResistanceMode(self):
        raise NotImplementedError, self
    
        
    def set4WireResistanceMode(self):
        raise NotImplementedError, self
   
        
    def setFrequencyMode(self):
        raise NotImplementedError, self


    def getDCVoltRange(self):
        raise NotImplementedError, self

    def takeMeasurement(self):
        raise NotImplementedError, self

    def verifyMode(self, mode):
        return self.currentMode == mode



class DmmVirtual(DmmBase):
    
    
    def __init__(self): #IGNORE:W0231 (we're not calling the parent constr)
        pass


    @modeCheck
    def setDcVoltsMode(self):
        pass


    @modeCheck
    def setAcVoltsMode(self):
        pass


    @modeCheck
    def setDcCurrentMode(self):
        pass


    @modeCheck
    def set2WireResistanceMode(self):
        pass


    @modeCheck
    def set4WireResistanceMode(self):
        pass


    @modeCheck
    def setFrequencyMode(self):
        pass


    def getDCVoltageRange(self):
        # TODO: Come up with a better return value?
        return 5.0 * random.randint(0, 100) * .01


    def takeMeasurement(self):
        # TODO: Come up with a better return value?
        # Can't be a static number as this messes up the 
        #    least square linear fit (used by smstrbs)
        return 5.0 * random.randint(0, 100) * .01



class DmmKeithley2750(DmmBase):
    '''
        Keithley 2750 DMM
    '''     
    
    @modeCheck
    def setDcVoltsMode(self):        
        self.__commonSetup()
        self.target.write(":FUNCtion 'VOLTage:DC'")
        self.target.write(":VOLTage:DC:RANGe:AUTO 1")        
        self.target.write(":VOLTage:DC:DIGits 7")     #Set DCV digit resolution
        self.target.write(":VOLTage:DC:AVERage:STATe OFF ")
        errorCheckKeithley27xx(self.target)


    @modeCheck
    def setAcVoltsMode(self):
        self.__commonSetup()
        self.target.write(":FUNCtion 'VOLT:AC'")
        self.target.write(":VOLTage:AC:RANGe:AUTO 1")        
        self.target.write(":VOLTage:AC:DIGits 7")     #Set ACV digit resolution
        self.target.write(":VOLTage:AC:AVERage:TCONtrol REPeat")
        self.target.write(":VOLTage:AC:AVERage:WINDow 1.0")
        self.target.write(":VOLTage:AC:AVERage:COUNt 20")
        self.target.write(":VOLTage:AC:AVERage:STATe ON ")
        errorCheckKeithley27xx(self.target)


    @modeCheck
    def setDcCurrentMode(self):
        self.__commonSetup()
        self.target.write(":FUNCtion 'CURR:DC'")
        self.target.write(":CURRent:DC:RANGe:AUTO 1")        
        self.target.write(":CURRent:DC:DIGits 7")     #Set DCC digit resolution
        self.target.write(":CURRent:DC:AVERage:TCONtrol REPeat")
        self.target.write(":CURRent:DC:AVERage:WINDow 1.0")
        self.target.write(":CURRent:DC:AVERage:COUNt 20")
        self.target.write(":CURRent:DC:AVERage:STATe ON ")
        errorCheckKeithley27xx(self.target)


    @modeCheck
    def set2WireResistanceMode(self):
        self.__commonSetup()
        self.target.write(":FUNCtion 'RES'")
        self.target.write(":RESistance:RANGe:AUTO 1")        
        self.target.write(":RESistance:DIGits 7")     #Set RES digit resolution
        self.target.write(":RESistance:AVERage:STATe OFF" )
        errorCheckKeithley27xx(self.target)


    @modeCheck
    def set4WireResistanceMode(self):
        self.__commonSetup()
        self.target.write(":FUNCtion 'FRES'")
        self.target.write(":FRESistance:RANGe:AUTO 1")        
        self.target.write(":FRESistance:DIGits 7")    #Set RES digit resolution
        self.target.write(":FRESistance:AVERage:STATe OFF ")
        errorCheckKeithley27xx(self.target)


    @modeCheck
    def setFrequencyMode(self):
        self.__commonSetup()
        self.target.write(":FUNCtion 'FREQ'")
        self.target.write(":FREQuency:DIGits 7")    #Set RES digit resolution
        self.target.write(":FREQuency:THReshold:VOLTage:RANGe 1")        
        errorCheckKeithley27xx(self.target)


    def takeMeasurement(self):
        self.target.write(":INIT:IMM")      
        self.target.write("*TRG")             
        self.target.write(":*OPC") #set bit 0 in ESR when done
        opc = 0
        while opc == 0:
            dmmStatus = ""
            while dmmStatus == "":
                dmmStatus = self.target.ask(":*ESR?")
            opc = int(dmmStatus) & 1
        result = self.target.ask(":FETC?")     
        errorCheckKeithley27xx(self.target)
        return result                          

      
    def setCalDates(self):
        '''
        Function to set the calibration dates in the DMM in case they are not
        set by the third party calibration company. Uncomment these lines and
        be sure that the DATE is the date the DMM was cal'd and the NDUE is
        the date when the DMM needs to be recal'd.
        '''
#        self.target.write(":CAL:PROT:CODE 'KI002750'")      
#        self.target.write(":CAL:PROT:INIT")      
#        self.target.write(":CAL:PROT:DATE 2008, 8, 26")      
#        self.target.write(":CAL:PROT:NDUE 2009, 8, 26")      
#        self.target.write(":CAL:PROT:SAVE")      
#        self.target.write(":CAL:PROT:LOCK")      
#        errorCheckKeithley27xx(self.target)
        pass

      
    def __commonSetup(self):
        self.target.write(":ABORt;*RST")    # NOTE: Opens all switches!
        self.target.write(":*CLS;:STATus:PRESet;:*ESE 1")
        self.target.write(":STATus:OPERation:ENABle 1024")
        self.target.write(":TRACe:CLEar:AUTO 1")
        self.target.write(":TRACe:POINts 55000")
        self.target.write(":TRACe:FEED CALCulate")
        self.target.write(":TRACe:FEED:CONTrol NEVer")
        self.target.write(":TRACe:CLEar")                                     
        self.target.write(":FORMat ASCii")   
        self.target.write(":FORMat:BORDer NORMal")      
        self.target.write(":INIT:CONT 0")      
        self.target.write(":SAMPle:COUNt 1")
        self.target.write(":SYSTem:AZERo:STATe 0")
        self.target.write(":TRIGger:SOURce BUS")
        self.target.write(":TRIGger:DELay 0.000000")
        self.target.write(":TRIGger:COUNt 1")
        self.target.write(":FORMat:ELEMents READ")
        self.target.write(":FREQ:APER 0.1")
        errorCheckKeithley27xx(self.target)


    def getDCVoltRange(self):
        return self.target.ask("VOLT:DC:RANG:UPP?")



def errorCheckKeithley27xx(target):
    '''
    This will poll the error queue until it is empty 
    and raises an exception if anything was in the queue
    '''

    errV = target.ask(":SYSTem:ERRor?")
    if errV == "":    # Allow one retry
        errV = target.ask(":SYSTem:ERRor?")
        if errV == "":
            raise pceExceptions.InstrumentException(
                                            "Instrument not responding")
    if errV[0] != '0':
        raise pceExceptions.InstrumentException(errV)              
