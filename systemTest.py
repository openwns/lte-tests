#! /usr/bin/env python
###############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2007
# Chair of Communication Networks (ComNets)
# Kopernikusstr. 16, D-52074 Aachen, Germany
# phone: ++49-241-80-27910,
# fax: ++49-241-80-22242
# email: info@openwns.org
# www: http://www.openwns.org
# _____________________________________________________________________________
#
# openWNS is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation;
#
# openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import os
import sys
base, tail = os.path.split(sys.argv[0])
os.chdir(base)

# Append the python sub-dir of WNS--main--x.y ...
sys.path.append(os.path.join('..', '..', '..', 'sandbox', 'default', 'lib', 'python2.4', 'site-packages'))

# ... because the module WNS unit test framework is located there.
import pywns.WNSUnit

# See if imtaphy module is available and adjust reference output
if os.path.exists("referenceOutput_config.py"):
    os.remove("referenceOutput_config.py")
if os.path.exists(os.path.join("..", "..", "..", "sandbox", "dbg", "lib", "PyConfig", "imtaphy")):
    os.symlink("referenceOutputIMTA_config.py", "referenceOutput_config.py")
    print "Using IMTA M2135 FastFading"
else: 
    print "Using Frequency Neighbor Correlated FastFading"
    os.symlink("referenceOutputFTFading_config.py", "referenceOutput_config.py")


# create a system test
testSuite1 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                    configFile = 'config.py',
                                    shortDescription = 'Basic InH config',
                                    runSimulations = True,
                                    disabled = False,
                                    disabledReason = "this will be displayed if you disable the suite")
testSuite2 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                    configFile = 'configVoIP.py',
                                    shortDescription = 'Basic InH config for VoIP',
                                    runSimulations = True,
                                    disabled = False,
                                    disabledReason = "this will be displayed if you disable the suite",
                                    maximumRelativeError = 1E-5)
testSuite3 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                    configFile = 'configMeta.py',
                                    shortDescription = 'Basic InH config including metascheduling',
                                    runSimulations = True,
                                    disabled = False,
                                    disabledReason = "this will be displayed if you disable the suite",
                                    maximumRelativeError = 1E-5)


# create a system test
testSuite = pywns.WNSUnit.TestSuite()
testSuite.addTest(testSuite1)
testSuite.addTest(testSuite2)
testSuite.addTest(testSuite3)
# If you want multiple test suites, just create another one and add it here
# e.g. testSuite.addTest(testSuite2)

if __name__ == '__main__':
    # This is only evaluated if the script is called manually

    # if you need to change the verbosity do it here
    # verbosity = 0 : No ouput
    # verbosity = 1 : Print one dot for each test, F for failure
    # verbosity = 2 : Prints the test name and status in a human readable way
    verbosity = 2

    pywns.WNSUnit.verbosity = verbosity

    # Create test runner
    testRunner = pywns.WNSUnit.TextTestRunner(verbosity=verbosity)

    # Finally, run the tests.
    testRunner.run(testSuite)
