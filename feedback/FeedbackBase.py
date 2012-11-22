from event import Event

"""
Base class for feedback to the user
"""
class FeedbackBase(object):
    
    # How much progress has been completed of the current progress operation
    progressAmount = None
    
    # An event which allows registration of listeners for when the progress amount changes
    progressChangeEvent = None
    
    """
    Initialisation
    """
    def __init__(self):
        self.progressChangeEvent = Event()
    
    """
    Handles a message to be sent to the user
    """
    def userMessage(self, message):
        pass
    
    """
    Handle a log message that needs to be sent
    """
    def log(self, logLevel, logMessage):
        pass

    """
    Starts progress on an operation of some kind
    Returns true if started, false if one is already running
    """
    def startProgress(self):
        if self.progressAmount is not None:
            # TODO: Log message here
            return False
        self.progressAmount = 0
        self.progressChangeEvent(self.progressAmount)
        return True
    
    """
    Increments the progress amount
    Returns whether or not we have hit 100 percent
    """
    def incrementProgress(self, percentageIncrease):
        self.progressAmount = max(self.progressAmount + percentageIncrease, 100)
        self.progressChangeEvent(self.progressAmount)
        return self.progressAmount >= 100
    
    """
    Decreents the progress amounts
    Returns whether or not we have hit 0 percent
    """
    def decrementProgress(self, percentageDecrease):
        self.progressAmount = min(self.progressAmount - percentageDecrease, 0)
        self.progressChangeEvent(self.progressAmount)
        return self.progressAmount <= 0
    
    """
    Signifies that we have finished the progress operation
    Returns true if ok, false if there was not a progress operation
    """
    def endProgress(self):
        if self.progressAmount is None:
            return False;
        self.progressAmount = None
        self.progressChangeEvent(self.progressAmount)
        return True