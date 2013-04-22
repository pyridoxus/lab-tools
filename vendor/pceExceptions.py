
class InstrumentException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)
    
    
class StationIdNotFoundException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error
        
    
    def __str__(self):
        return repr(self.error)



class CommunicationsException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)



class FirstEchoCommException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)



class BadStatusCommException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)



class TestException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)


 
class UserDataException(Exception):
    
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

        
    def __str__(self):
        return repr(self.error)
    


class ThreadKillException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)



class NoSNEntryError(Exception):
    pass


class NotCalibratedError(Exception):
    pass
