from FeedbackBase import FeedbackBase
from LogLevels import LogLevels

class ConsoleFeedback(FeedbackBase):
    
    """
    Initialises and registers the callback for progress change events
    """
    def __init__(self):
        super(ConsoleFeedback, self).__init__()
        
        self.progressChangeEvent += self.progressChange
        
    """
    Callback for progress change events
    """
    def progressChange(self, complete):
        print "Progress: %s" % complete
    
    def userMessage(self, message):
        print "MSG: %s" % message
    
    def log(self, logLevel, message):
        print "%s: %s" % (LogLevels().getLevel(logLevel), message)