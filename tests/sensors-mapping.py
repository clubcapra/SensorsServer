#!/bin/usr/python

import unittest
import tempfile
import os

# add src folder in path to resolve imports
import sys
sys.path.append("src/")
sys.path.append("tests/")

from sensors_mapping import SensorsMapping

class SensorsMappingTest(unittest.TestCase):

    def testIsValidId(self):
        mapping = SensorsMapping()

        self.assertTrue(mapping.isValidId("3"))
        self.assertFalse(mapping.isValidId("-1"))
        self.assertFalse(mapping.isValidId("8"))


    def testParseLines(self):
        lines = ["RangeFinder = 1", \
                 "GPS         = 2"]

        mapping = SensorsMapping()
        mapping.parseLines(lines)

        self.assertEqual(0, mapping.getErrorCount())
        self.assertEqual(1, mapping.getValues()["RangeFinder"])
        self.assertEqual(2, mapping.getValues()["GPS"])


    def testLoad(self):
        filename = tempfile.mktemp()
        f = open(filename, 'w')
        f.write("RangeFinder = 1\n")
        f.write("GPS         = 2\n")
        f.close()

        mapping = SensorsMapping()
        mapping.load(filename)
        os.unlink(filename)

        self.assertEqual(0, mapping.getErrorCount())
        self.assertEqual(1, mapping.getValues()["RangeFinder"])
        self.assertEqual(2, mapping.getValues()["GPS"])


if __name__ == "__main__":
    unittest.main()

