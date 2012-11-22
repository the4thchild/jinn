
class LogLevels(object):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARN = 4
    ERROR = 5
    
    def getLevel(self, level):
        if level == 1:
            return "TRACE"
        elif level == 2:
            return "DEBUG"
        elif level == 3:
            return "INFO"
        elif level == 4:
            return "WARN"
        elif level == 5:
            return "ERROR"
        else:
            return "LOG"