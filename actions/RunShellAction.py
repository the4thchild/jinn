from action.ActionBase import ActionBase
import os
import g
from feedback.LogLevels import LogLevels

class RunShellAction(ActionBase):
    
    def getType(self):
        return "Jinn::Action::RunShell"
    
    def run(self, args):
        cmd = self.getProperty("Command") + " " + args
        res = os.system(cmd)
        g.feedback.log(LogLevels.DEBUG, "Running command %s resulted in code %s" % (cmd, str(res)))
        return res is 0