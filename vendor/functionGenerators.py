
from Instruments.instrument import gpibInstrument

from Instruments.Support import connInterface

from Instruments.Support.pceExceptions import InstrumentException

name = "Function Generator"


class FunctionGeneratorsBase(gpibInstrument):
    '''
        Function Generators abstract base class, do not instantiate
    '''

    def __init__(self, gpibIp, instrId):
        self.target = connInterface.connectToInstrumentOverGpib(gpibIp, instrId)
        try:
            self._errorCheck()
        except InstrumentException:
            try:
                #sometimes can get false errors after rebooting cal stand
                self._errorCheck()  #do it again in case the error was false
            except InstrumentException:
                raise
            


    def _setWaveform(self, function, low_voltage, high_voltage, frequency):
        raise NotImplementedError, self


    def _errorCheck(self):
        raise NotImplementedError, self
    
    
    def setDcVoltage(self, voltage):
        raise NotImplementedError, self

        
    def setSquareWave(self, low_voltage, high_voltage, frequency):
        raise NotImplementedError, self

        
    def setSineWave(self, low_voltage, high_voltage, frequency):
        raise NotImplementedError, self



class FunctionGeneratorsVirtual(FunctionGeneratorsBase):
    '''
        A virtual function generator.
    '''

    def __init__(self): #IGNORE:W0231 (we're not calling the parent constr)
        pass


    def setDcVoltage(self, voltage):
        pass

        
    def setSquareWave(self, low_voltage, high_voltage, frequency):
        pass

        
    def setSineWave(self, low_voltage, high_voltage, frequency):
        pass
    


class FunctionGeneratorsSrs360(FunctionGeneratorsBase):
    '''
        Stanford Research Systems SRS360 Function Generator
    '''
    
    def __init__(self, gpibIp, instrId):
        FunctionGeneratorsBase.__init__(self, gpibIp, instrId)


    def _setWaveform(self, function, low_voltage, high_voltage, frequency):
        amplitude = float(high_voltage) - float(low_voltage)
        offset = (float(high_voltage) + float(low_voltage)) / 2.0
        self.target.write(function)
        self.target.write("FREQ %f" % frequency)
        self.target.write("AMPL %fVP" % amplitude)
        self.target.write("OFFS %f" % offset)
        self._errorCheck()

        
    def _errorCheck(self):
        esr = self.target.ask("*ESR?")
        if int(esr) != 0:
            message = "Bad ESR status = 0x%02X" % int(esr)
            raise InstrumentException(message)
                

    def setDcVoltage(self, voltage):
        self.target.write("FUNC 1")
        self.target.write("FREQ 0.01")
        self.target.write("AMPL 0VP")
        self.target.write("OFFS %f" % voltage)
        self._errorCheck()

        
    def setSquareWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("FUNC 1", low_voltage, high_voltage, frequency)

        
    def setSineWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("FUNC 0", low_voltage, high_voltage, frequency)


    
class FunctionGeneratorsAgilent33120A(FunctionGeneratorsBase):
    '''
        Agilent/HP 33120A Function Generator
    '''
    
    def __init__(self, gpibIp, instrId):
        FunctionGeneratorsBase.__init__(self, gpibIp, instrId)
 
        
    def _setWaveform(self, function, low_voltage, high_voltage, frequency):
        amplitude = float(high_voltage) - float(low_voltage)
        offset = (float(high_voltage) + float(low_voltage)) / 2.0
        self.target.write("VOLTage %f" % amplitude)
        self.target.write("VOLTage:OFFSet %f" % offset)
        self.target.write("FREQuency %f" % frequency)
        self.target.write("OUTPut:LOAD MAX")
        self.target.write("FUNCtion:SHAPe %s" % function)
        self._errorCheck()

        
    def _errorCheck(self):
        esr = self.target.ask("*ESR?")
        if int(esr) != 0:
            message = "Bad ESR status = 0x%02X" % int(esr)
            raise InstrumentException(message)
        
                
    def setDcVoltage(self, voltage):
        self.target.write("APPLy:DC DEFault, DEFault, %f" % voltage)
        self._errorCheck()

        
    def setSquareWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("SQUare", low_voltage, high_voltage, frequency)

        
    def setSineWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("SINusoid", low_voltage, high_voltage, frequency)
        
        

class FunctionGeneratorsAgilent33220A(FunctionGeneratorsBase):
    '''
        Agilent/HP 33220A Function Generator
    '''
    
    def __init__(self, gpibIp, instrId):
        FunctionGeneratorsBase.__init__(self, gpibIp, instrId)
 
        
    def _setWaveform(self, function, low_voltage, high_voltage, frequency):
        amplitude = float(high_voltage) - float(low_voltage)
        offset = (float(high_voltage) + float(low_voltage)) / 2.0
        self.target.write("VOLTage %f" % amplitude)
        self.target.write("VOLTage:OFFSet %f" % offset)
        self.target.write("FREQuency %f" % frequency)
        self.target.write("OUTPut:LOAD INFinity")
        self.target.write("OUTPut ON")
        self.target.write("FUNCtion:SHAPe %s" % function)
        self._errorCheck()

        
    def _errorCheck(self):
        esr = self.target.ask("*ESR?")
        if int(esr) != 0:
            message = "Bad ESR status = 0x%02X" % int(esr)
            raise InstrumentException(message)
        
                
    def setDcVoltage(self, voltage):
        self.target.write("APPLy:DC DEFault, DEFault, %f" % voltage)
        self._errorCheck()

        
    def setSquareWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("SQUare", low_voltage, high_voltage, frequency)

        
    def setSineWave(self, low_voltage, high_voltage, frequency):
        self._setWaveform("SINusoid", low_voltage, high_voltage, frequency)
