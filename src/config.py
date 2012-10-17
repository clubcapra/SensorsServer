import string

class Config:
    
    def __init__(self):
        self.errorCount = 0
        self.values = {}
        pass


    def load(self, configPath):
        self.parseLines(open(configPath).readlines())
        self.afterLoad();

    def afterLoad(self):
        pass


    def parseLines(self, lines):
        lineNumber = 0
        for line in lines:
            # remove \n
            line = line.replace("\n", "")
            # count line
            lineNumber = lineNumber + 1

            # check if its a comment
            if line.startswith("#"):
                continue

            # ignore empty lines
            if string.strip(line, " \t") == "":
                continue
            
            # check if its contains a =
            if line.find("=") == -1:
                print "Warning line " + str(lineNumber) + " does not contain an equals"
                print "\t\t" + line
                self.errorCount += 1
                continue

            # check for user specific validation
            if not self.lineIsValid(line):
                self.errorCount += 1
                continue

            # add line information to the values
            self.processLine(line)


    # must be defined by hineritance
    def lineIsValid(self, line):
        return True


    # must be defined by hineritance
    def processLine(self, line):
        parts = string.split(line, "=")
        self.values[string.strip(parts[0], " \t")] = string.strip(parts[1], " \t")


    def getErrorCount(self):
        return self.errorCount


    def getValues(self):
        return self.values

