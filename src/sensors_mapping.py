import config
import string

class SensorsMapping(config.Config):

    def processLine(self, line):
        parts = string.split(line, "=")
        self.values[string.strip(parts[0], " \t")] = int(string.strip(parts[1], " \t"))


    def lineIsValid(self, line):
        parts = string.split(line, "=")
        if not self.isValidId(string.strip(parts[1], " \t")):
            print "Warning line " + str(lineNumber) + " does not refer to digit from 0 to 7"
            return False
        return True
                

    def isValidId(self, identifier):
        if not identifier.isdigit():
            return False

        if not int(identifier) >= 0:
            return False

        if not int(identifier) <= 7:
            return False

        return True

