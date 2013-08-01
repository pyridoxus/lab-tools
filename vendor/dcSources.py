
from time import sleep, clock

from instrument import gpibInstrument
from pceExceptions import InstrumentException, ThreadKillException

name = "DC Source"


class DcSourcesBase(gpibInstrument):
    '''
        DC sources abstract base class, do not instantiate
    '''
    
    def __init__(self, gpibIp, instrId, roe = 1):
        gpibInstrument.__init__(self, gpibIp, instrId, roe)
        #the following are to be set by the subclasses
        #when calling _getSettleRange()
        self.highSettleLimit = 0.0
        self.lowSettleLimit = 0.0
    
    
    def setDcVoltage(self, voltage):
        raise NotImplementedError, self


    def _getSettleRange(self, voltage):
        raise NotImplementedError, self
    
    
    def _setFloatGround(self):
        raise NotImplementedError, self
    
    
    def _set2Wire(self):
        raise NotImplementedError, self
    
    
    def _dcSourceSettle(self, dmmMeasureFunction, terminateEvent):
        '''
        This function uses the DMM to make sure the DC Source is very close
        to the requested voltage before returning back to the calling function.
        The DMM MUST be set to DCVOLTS mode before setting the DC Source.
        The SWITCH MATRIX MUST be setup so that the DMM can measure the
        DC Source before setting the DC Source voltage.
        NOTE: self.highSettleLimit and self.lowSettleLimit must be set using the
        derived class' getSettleRange() before calling this function!
        '''
        t = clock()
        for maxMeasurements in range(10):
            if terminateEvent is not None:
                if terminateEvent.isSet() == True:
                    raise ThreadKillException("TERMINATED BY USER")
            measuredVoltage = (float)(dmmMeasureFunction())
            if measuredVoltage < self.highSettleLimit and\
                    measuredVoltage > self.lowSettleLimit:
                break
        s = clock()
#        print "DCSOURCE settled in %f seconds" % (s - t)


    def setDcVoltageWithSettle(self, voltage, dmmMeasureFunction,
                                terminateEvent = None):
        '''
        Sets the DC Voltage but does not return until the output voltage is
        within the voltage range determined by the settling range. To use this
        function, the DMM must already be in DCVOLTS mode and the switch matrix
        must already have the DMM and the DC SOURCE connected together.
        '''
        self.setDcVoltage(voltage)  #set voltage as usual
        self._getSettleRange(voltage) #setup the range
        self._dcSourceSettle(dmmMeasureFunction, terminateEvent)
        


class DcSourcesVirtual(DcSourcesBase):
    
    def __init__(self): #IGNORE:W0231 (we're not calling the parent constr)
        pass
    
    def setDcVoltage(self, voltage):
        '''
        On setDCVoltage, Virtual Hardware should pass silently.
        '''
        pass 


    def _getSettleRange(self, voltage):
        '''
        Virtual DC Source really doesn't need to "settle", so allow any
        possible value to be a good value.
        '''
        self.highSettleLimit = voltage + 1000.0
        self.lowSettleLimit = voltage - 1000.0



class DcSourcesKrohnHiteEdcSeries(DcSourcesBase):
    '''
        Krohn Hite EDC 521/522 DC Calibrator abstract base class
    '''
    
    def __init__(self, gpibIp, instrId):
        DcSourcesBase.__init__(self, gpibIp, instrId)
        self.voltage_ranges = []
        self.last_range = None
        self.target.ask("?")


    def setDcVoltage(self, voltage):
        programming_string = None
        if voltage == 0.0:
            new_range = 0
            self.target.write("00000000")
            if self.last_range == new_range:
                sleep(0.005)
            else:
                sleep(0.3)
            self.last_range = new_range
            self.target.ask("?")    # Clear the Data Error
            return
        else:
            for vr in self.voltage_ranges:
                if abs(voltage) < vr['Max Voltage']:
                    digits_string = "%.6d" % (int(abs(voltage) * \
                                                      vr['Multiplier']))
                    programming_string = "%c%s%c" % (
                                                ('+' if voltage > 0 else '-'), 
                                                digits_string, 
                                                vr['Range Specifier'])
                    new_range = vr['Max Voltage']
                    break
        if programming_string == None:
            raise InstrumentException(
                                        "Requested voltage out of range")
        self.target.write(programming_string)
        if self.last_range == new_range:
            sleep(0.005)
        else:
            sleep(0.3)
        self.last_range = new_range
        if self.target.ask("?") != "NOTHING WRONG":
            raise InstrumentException("Programming Error")


    def appendVoltageRange(self, voltageRanges):
        for maxV, spec, mult in voltageRanges:
            self.voltage_ranges.append({'Max Voltage':maxV,
                                        'Range Specifier':spec,
                                        'Multiplier': mult})



class DcSourcesKrohnHiteEdc521(DcSourcesKrohnHiteEdcSeries):
    '''
        Krohn Hite EDC 521 DC Calibrator
    '''
    def __init__(self, gpibIp, instrId):
        DcSourcesKrohnHiteEdcSeries.__init__(self, gpibIp, instrId)
        self.appendVoltageRange([[0.100, "0", 10000000.0],
                                 [10.00, "1", 100000.0],
                                 [100.0, "2", 10000.0]])


    def _getSettleRange(self, voltage):
        '''
        For the EDC521, set the upper and lower ranges for settling depending
        on the requested voltage.
        '''
        #The settle limits are from INS - Instrumentation/INS-0010 Krohn-Hite
        #Model 521 Electronic DC Calibrator/INS-0010-00 (2007-05-02)/EDC
        #Calibrator Model 521 Specs.htm
        #    +/-(0.002% of setting + 0.0005% of range + 3uV)

        voltageRange = [100.0, 10.0, 0.1, -0.1, -10.0, -100.0]
        for range in voltageRange:
            if voltage > range:
                break
        delta = 0.00002 * voltage + 0.000005 * range + 3E-6

        self.highSettleLimit = voltage + delta
        self.lowSettleLimit = voltage - delta



class DcSourcesKrohnHiteEdc521With1000vOption(DcSourcesKrohnHiteEdc521):
    '''
        Krohn Hite EDC 521 DC Calibrator
    '''
    def __init__(self, gpibIp, instrId):
        DcSourcesKrohnHiteEdc521.__init__(self, gpibIp, instrId)
        self.appendVoltageRange([[1000.0, "3", 1000.0]])


    def _getSettleRange(self, voltage):
        '''
        For the EDC521 with 1000v option, set the upper and lower ranges for
        settling depending on the requested voltage.
        '''
        #The settle limits are from INS - Instrumentation/INS-0010 Krohn-Hite
        #Model 521 Electronic DC Calibrator/INS-0010-00 (2007-05-02)/EDC
        #Calibrator Model 521 Specs.htm
        #    +/-(0.002% of setting + 0.0005% of range + 3uV)

        voltageRange = [1000.0, 100.0, 10.0, 0.1, -0.1, -10.0, -100.0, -1000.0]
        for range in voltageRange:
            if voltage > range:
                break
        delta = 0.00002 * voltage + 0.000005 * range + 3E-6

        self.highSettleLimit = voltage + delta
        self.lowSettleLimit = voltage - delta
        


class DcSourcesKrohnHiteEdc522WithRA7Option(DcSourcesKrohnHiteEdcSeries):
    '''
        Krohn Hite EDC 522 DC Calibrator with RA7 Option
    '''
    def __init__(self, gpibIp, instrId):
        DcSourcesKrohnHiteEdcSeries.__init__(self, gpibIp, instrId)
        self.appendVoltageRange([[0.100, "0", 10000000.0],
                                 [1.000, "1", 1000000.0],
                                 [10.00, "2", 100000.0],
                                 [100.0, "3", 10000.0]])


    def _getSettleRange(self, voltage):
        '''
        For the EDC522 with RA7 option, set the upper and lower ranges for
        settling depending on the requested voltage.
        '''
        pass



class DcSourcesKrohnHiteEdc523(DcSourcesBase):
    '''
        Krohn Hite EDC 523 DC Calibrator class
    '''
    
    def __init__(self, gpibIp, instrId, roe = 1):
        DcSourcesBase.__init__(self, gpibIp, instrId, roe)


    def crowBar(self, crowBarState = "ON"):
        '''
        Turn the crowbar on or off.
        Default: ON
        Not sure if this function is the same for the EDC521 or not.
        If so, then this function should become a member of the DcSourcesBase.
        '''
        if crowBarState == "ON":
            self.target.write("Z")
        else:
            self.target.write("V")
        
        
    def _getSettleRange(self, voltage):
        '''
        For the EDC523, set the upper and lower ranges for settling depending
        on the requested voltage.
        '''
        #Voltage specs are from the documentation (Krohn-Hite_523_manual.pdf)
        #Unfortunately due to internal cal stand resistances, it seems unlikely
        #to ever achieve the 8ppm accuracy.
        if voltage > 0.0:
            self.highSettleLimit = voltage * 1.000050
            self.lowSettleLimit = voltage * 0.999950
        if voltage < 0.0:
            self.highSettleLimit = voltage * 0.999950
            self.lowSettleLimit = voltage * 1.000050
        if voltage == 0.0:
            self.highSettleLimit = 0.000016
            self.lowSettleLimit = -0.000016


    def setDcVoltage(self, voltage):
        self._setFloatGround()
        self._set2Wire()
        voltage = float(voltage)
        if abs(voltage) < 0.001:
            programming_string = "%fuV" % (voltage * 1000000)
        elif abs(voltage) < 1.0:
            programming_string = "%fmV" % (voltage * 1000)
        elif abs(voltage) < 100.0:
            programming_string = "%fV" % (voltage)
        else:
            raise InstrumentException(
                                        "Requested voltage out of range")
            
        self.target.write(programming_string)


    def _setFloatGround(self):
        '''
        Set the ground to float. This prevents the internal ground from being
        connected to the chassis, which causes voltage measurement failures
        during tests.
        '''
        self.target.write("f")


    def _set2Wire(self):
        '''
        Set the output to be 2 wire termination. Voltage will be incorrect if
        the DC Source enters 4 wire for some reason.
        '''
        self.target.write("2w")
