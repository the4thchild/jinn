
class LogLevels:
    DEBUG = 1
    INFO  = 2
    WARN  = 3
    ERROR = 4
    
    @staticmethod
    def getLevel(level):
        if level == 1:
            return "DEBUG"
        elif level == 2:
            return "INFO"
        elif level == 3:
            return "WARN"
        elif level == 4:
            return "ERROR"
        else:
            return "INFO"
    
    @staticmethod 
    def getLevelFromString(levelStr):
        if levelStr == "DEBUG":
            return 1
        elif levelStr == "INFO":
            return 2
        elif levelStr == "WARN":
            return 3
        elif levelStr == "ERROR":
            return 4
        else:
            return 2