'''
Base abstract instrument classes to join all Vendor and SoMat instrument objects
'''

from Instruments.Support import utils

class Instrument(object):
    
    def _getUniqueIdent(self):
        raise NotImplementedError, self



class gpibInstrument(Instrument):
    
    def _getUniqueIdent(self, instrObj):
        gpibIdent = instrObj.target.ask("*IDN?")
        
        manufSN = gpibIdent.split(",")[2]
        
        return manufSN



class ethernetInstrument(Instrument):
    
    def _getUniqueIdent(self, instrObj):
        macIdent = utils.get_macaddress(instrObj.ip_address)
        
        return macIdent

        