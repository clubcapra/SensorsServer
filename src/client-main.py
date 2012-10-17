#!/usr/bin/python

import sys
import string

# this is how we create a class in python
class ClassExample:
    x = 101; # declaring a member variable

    def __init__(self):
        pass

    # a method always have self as first argument
    def getX(self):
        print "Calling getX - showing x value:" + str(self.x)


def usage():
    print "the usage should be defined here."

def main():
    print "This is the client-main"

    # print arguments
    print "  arguments: " + string.join(sys.argv, ", ")

    # manipulating objects
    c = ClassExample()
    c.getX()

if __name__ == "__main__":
    main()

