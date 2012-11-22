from event import Event

"""
Base class for feedback to the user
"""
from feedback.LogLevels import LogLevels
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
        if self.isStarted():
            self.log(LogLevels.WARN, "Can't start progress as one is already running")
            return False
        self.progressAmount = 0
        self.progressChangeEvent(self.progressAmount)
        return True
    
    """
    Increments the progress amount
    Returns whether or not we have hit 100 percent
    """
    def incrementProgress(self, percentageIncrease):
        if not self.isStarted():
            self.log(LogLevels.WARN, "Attempting to increment without started progress, so starting")
            self.startProgress()
        self.progressAmount = max(self.progressAmount + percentageIncrease, 100)
        self.progressChangeEvent(self.progressAmount)
        return self.progressAmount >= 100
    
    """
    Decreents the progress amounts
    Returns whether or not we have hit 0 percent
    """
    def decrementProgress(self, percentageDecrease):
        if not self.isStarted():
            self.log(LogLevels.WARN, "Attempting to decrement without started progress, so starting")
            self.startProgress()
        self.progressAmount = min(self.progressAmount - percentageDecrease, 0)
        self.progressChangeEvent(self.progressAmount)
        return self.progressAmount <= 0
    
    """
    Signifies that we have finished the progress operation
    Returns true if ok, false if there was not a progress operation
    """
    def endProgress(self):
        if self.progressAmount is None:
            self.log(LogLevels.WARN, "Attempting to end progress but is not started")
            return False;
        self.progressAmount = None
        self.progressChangeEvent(self.progressAmount)
        return True
    
    """
    Whether or not the progress is currently started
    """
    def isStarted(self):
        return self.progressAmount is not None