
from types import StringType

from instrument import gpibInstrument
from pceExceptions import InstrumentException

name = "Switch matrices"


class SwitchMatrixBase(gpibInstrument):
    '''
        switch matrix abstract base class, do not instantiate 
    '''
    
    def openAllSwitches(self):
        raise NotImplementedError, self
        
        
    def openSwitch(self, instrument, cpc_connector_pinpair_tuple):
        raise NotImplementedError, self
        
        
    def closeSwitch(self, instrument, cpc_connector_pinpair_tuple):
        raise NotImplementedError, self
        
        
    def openAllHighCurrentSwitches(self):
        raise NotImplementedError, self
        
        
    def openHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self
        
        
    def closeHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self
    
    
    def resolveInstrument(self, instrument):
        if type(instrument) != StringType:
            return instrument
        return self.instrument_dictionary[instrument]



class SwitchMatrixVirtual(SwitchMatrixBase):
    
    def __init__(self, instrument_dictionary): #IGNORE:W0231
        pass


    def openAllSwitches(self):
        pass
        
        
    def openSwitch(self, instrument, cpc_connector_pinpair_tuple):
        pass
        
        
    def closeSwitch(self, instrument, cpc_connector_pinpair_tuple):
        pass
        
        
    def openAllHighCurrentSwitches(self):
        pass
        
        
    def openHighCurrentSwitch(self, switch_number):
        pass
        
        
    def closeHighCurrentSwitch(self, switch_number):
        pass
    
        

class SwitchMatrixKeithley2750(SwitchMatrixBase):
    '''
        Class for switch matrix inside Keithley 2750 DMM
    '''
    # Keithley 2750 DMM with 5 slot Switch Mainframe with 
    # the following cards installed:
    #    Keithley 7702 - 40 Channel Mux in slots 1 through 4
    #    Keithley 7709 - 6x8 Matrix in slot 5
    #
    #
    # Close XYY
    # Close 5ZZ
    #
    # Where:
    # X = 1, for "CS" Testpoint = 1 to 40
    # X = 2, for "CS" Testpoint = 41 to 80
    # X = 3, for "CS" Testpoint = 81 to 120
    # X = 4, for "CS" Testpoint = 121 to 160

    # YY = ("CS" Testpoint), for "CS" Testpoint = 1 to 40
    # YY = ("CS" Testpoint - 40), for "CS" Testpoint = 41 to 80
    # YY = ("CS" Testpoint - 80), for "CS" Testpoint = 81 to 120
    # YY = ("CS" Testpoint - 120), for "CS" Testpoint = 121 to 160

    # ZZ = (("CS" Instrument - 1) * 8) +
    # 1, for "CS" Testpoint = 1 to 20
    # 2, for "CS" Testpoint = 21 to 40
    # 3, for "CS" Testpoint = 41 to 60
    # 4, for "CS" Testpoint = 61 to 80
    # 5, for "CS" Testpoint = 81 to 100
    # 6, for "CS" Testpoint = 101 to 120
    # 7, for "CS" Testpoint = 121 to 140
    # 8, for "CS" Testpoint = 141 to 160
    #
    
    instrument_dictionary = {
                             'DMM' : 1,
                             'DMM_SENSE' : 2,
                             'FGEN' : 3,
                             'DCSOURCE' : 4,
                             'ELOAD' : 5,
                             'XOVER' : 6,
                             }
    
        
    def __computeTestPointNumber(self, cpc_connector_pinpair_tuple):
        # cpc_connector = ( 1 to 10 )
        # cpc_pinpair = ( 1 to 16 )
        # returns ( 1 to 160 )
        cpc_connector, cpc_pinpair = cpc_connector_pinpair_tuple
        return (cpc_pinpair - 1) * 10 + cpc_connector


    def __formatSwitchString(self, instrument, test_point):
        if (instrument < 1) or (instrument > 6):
            raise InstrumentException, ("Inputs out of range:" +
                    "\t Instrument (% s) must not be  < 1 or > 6" % instrument)
        
        if (test_point < 1) or (test_point > 160):
            raise InstrumentException, ("Inputs out of range:" +
                    "\t Testpoint (% s) must not be < 1 or > 160" % test_point)
            
        if test_point <= 20:
            x = 1
            yy = test_point
            zz = ((instrument - 1) * 8) + 1
        elif test_point <= 40:
            x = 1
            yy = test_point
            zz = ((instrument - 1) * 8) + 2
        elif test_point <= 60:
            x = 2
            yy = test_point - 40
            zz = ((instrument - 1) * 8) + 3
        elif test_point <= 80:
            x = 2
            yy = test_point - 40
            zz = ((instrument - 1) * 8) + 4
        elif test_point <= 100:
            x = 3
            yy = test_point - 80
            zz = ((instrument - 1) * 8) + 5
        elif test_point <= 120:
            x = 3
            yy = test_point - 80
            zz = ((instrument - 1) * 8) + 6
        elif test_point <= 140:
            x = 4
            yy = test_point - 120
            zz = ((instrument - 1) * 8) + 7
        else:
            x = 4
            yy = test_point - 120
            zz = ((instrument - 1) * 8) + 8
        switch_string = "(@ %01d%02d,%01d43,5%02d,549,550)" % (x, yy, x, zz)
        return switch_string
    
    
    def openAllSwitches(self):
        self.target.write(":ROUTE:OPEN:ALL")
#         errorCheckKeithley27xx(self.target)


    def openSwitch(self, instrument, cpc_connector_pinpair_tuple):
        test_point = self.__computeTestPointNumber(cpc_connector_pinpair_tuple)
        self.target.write(":ROUTE:MULT:OPEN %s" % 
                          self.__formatSwitchString(
                            self.resolveInstrument(instrument), test_point))
#         errorCheckKeithley27xx(self.target)


    def closeSwitch(self, instrument, cpc_connector_pinpair_tuple):
        test_point = self.__computeTestPointNumber(cpc_connector_pinpair_tuple)
        self.target.write(":ROUTE:MULT:CLOS %s" % 
                          self.__formatSwitchString(
                            self.resolveInstrument(instrument), test_point))
#         errorCheckKeithley27xx(self.target)
           
            
    def openAllHighCurrentSwitches(self):
        raise NotImplementedError, self
        
        
    def openHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self
        
        
    def closeHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self
        


class SwitchMatrixKeithley7002(SwitchMatrixBase):
    '''
        Class for Keithley 7002 switch matrix
    '''
    
    # Keithley 7002 Switch Mainframe with the following cards installed:
    #     Jumpers removed so that slots 1-5 are isolated from slots 6-10
    #     Keithley 7012-S 4x10 Matrix cards in slots 1 and 6
    #     The 10 outputs from the matrix cards are connected in parallel
    #     Keithley 7011-S Quad 1x10 Multiplexor cards in slots 2 and 7
    # 
    #  The resulting configuration allows for any one of the 80 
    #  test point pairs to be connected to any or all of the 10 
    #  instruments wired to the back panel. The relays on the 7053 
    #  are independant of all test points and instruments, but are 
    #  wired in parallel with each other, so in more that one is 
    #  actuated at a time, they will be connected together, as well 
    #  as to the common connection
    #  
    # 
    #  Computation of (instrument, test_point) pair to Keithley 7002 channels
    # 
    #  General form is a pair of switch addresses needed to connect 
    #  1 of 80test_point pairs to 1 of 10 instruments.  The printf 
    #  format string would look the following:
    # 
    #  viPrintf("(@ %d!%d,%d!%d!%d)", mux_slot, mux_channel, 
    #                                 matrix_slot, matrix_row, matrix_col);
    # 
    #  Given that 1 <= instrument <= 10 and 1 <= test_point <= 80, then
    # 
    #  mux_slot = test_point <= 40 ? 2 : 7;
    #  mux_channel = test_point <= 40 ? test_point : test_point - 40;
    #  matrix_slot = mux_slot - 1;
    #  matrix_row = ((mux_channel - 1) / 10) + 1;
    #  matrix_col = instrument;
    # 
    # 
    
    def __computeTestPointNumber(self, cpc_connector_pinpair_tuple):
        # cpc_connector = ( 1 to 5 )
        # cpc_pinpair = ( 1 to 16 )
        # returns ( 1 to 80 )
        cpc_connector, cpc_pinpair = cpc_connector_pinpair_tuple
        return (2 * (((cpc_pinpair - 1) / 2) * 5) + 
                (((cpc_pinpair - 1) & 1) + 1) + ((cpc_connector - 1) * 2))

    
    def __formatSwitchString(self, instrument, test_point):
        if ((instrument < 1) or (instrument > 10) or 
            (test_point < 1) or (test_point > 80)):
            raise InstrumentException, "Inputs out of range"
        if(test_point <= 40):
            mux_slot = 2
            mux_channel = test_point
        else:
            mux_slot = 7
            mux_channel = test_point - 40
        matrix_slot = mux_slot - 1
        matrix_row = ((mux_channel - 1) / 10) + 1
        matrix_col = instrument
        switch_string = ("(@ %d!%d,%d!%d!%d)" % 
                         (mux_slot, mux_channel, matrix_slot, 
                          matrix_row, matrix_col))
        return switch_string
 
        
    def _errorCheck(self):
        errV = self.target.ask("*ESR?")
        if errV == "*ESR 16":
            raise InstrumentException, "Nonextant command received"
        elif errV == "*ESR 32":
            raise InstrumentException, "Inexecutable command received"


    def openAllSwitches(self):
        self.target.write(":ROUTE:OPEN ALL")
        self._errorCheck()       

        
    def openSwitch(self, instrument, cpc_connector_pinpair_tuple):
        test_point = self.__computeTestPointNumber(cpc_connector_pinpair_tuple)
        self.target.write(":ROUTE:OPEN %s" % 
                          self.__formatSwitchString(
                            self.resolveInstrument(instrument), test_point))
        self._errorCheck()


    def closeSwitch(self, instrument, cpc_connector_pinpair_tuple):
        test_point = self.__computeTestPointNumber(cpc_connector_pinpair_tuple)
        self.target.write(":ROUTE:CLOSE %s" % 
                          self.__formatSwitchString(
                            self.resolveInstrument(instrument), test_point))
        self._errorCheck()


    def openAllHighCurrentSwitches(self):
        raise NotImplementedError, self
  
        
    def openHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self
  
        
    def closeHighCurrentSwitch(self, switch_number):
        raise NotImplementedError, self



class SwitchMatrixKeithley7002WithHighCurrentSwitching(
                                                    SwitchMatrixKeithley7002):
    '''
        Keithley 7002 switch matrix w/ a high current switch card added
    '''

    #
    # The high current switch card is install in slot 3
    #     Keithley 7053 10-Channel, 2-Pole, High Current Scanner card in slot 3 
    #       The 0-Ohm jumpers are removed on all 10 channels
    #
    #  switches (relays) are numbered 1 through 10
    #

    def __formatHighCurrentSwitchString(self, switch_number):
        if (switch_number < 1) or (switch_number > 10):
            raise InstrumentException, "Input out of range"
        switch_string = "(@ 3!%d)" % switch_number
        return switch_string
    
    
    def openAllHighCurrentSwitches(self):
        self.target.write(":ROUTE:OPEN (@ 3!1:3!10)")
        self._errorCheck()
     
        
    def openHighCurrentSwitch(self, switch_number):
        self.target.write(":ROUTE:OPEN %s" % 
                          self.__formatHighCurrentSwitchString(switch_number))
        self._errorCheck()
     
        
    def closeHighCurrentSwitch(self, switch_number):
        self.target.write(":ROUTE:CLOSE %s" % 
                          self.__formatHighCurrentSwitchString(switch_number))
        self._errorCheck()
