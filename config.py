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

from scenarios.ituM2135.placer import IndoorHotspotBSPlacer, IndoorHotspotUEPlacer
from scenarios.ituM2135.antenna import IndoorHotspotAntennaCreator
from scenarios.ituM2135.channelmodelcreator import IndoorHotspotChannelModelCreator
from scenarios.builders.creatorplacer import CreatorPlacerBuilder

from lte.creators.fdd import BSCreator, UECreator
import lte.support.helper

class Config:
    modes = ["ltefdd10"]

bsPlacer = IndoorHotspotBSPlacer()
uePlacer = IndoorHotspotUEPlacer(numberOfNodes = 1, minDistance = 3)
bsCreator = BSCreator(Config)
bsAntennaCreator = IndoorHotspotAntennaCreator()
ueCreator = UECreator(Config)
channelModelCreator = IndoorHotspotChannelModelCreator()

CreatorPlacerBuilder(bsCreator, bsPlacer, bsAntennaCreator, ueCreator, uePlacer, channelModelCreator)

import openwns.simulator

sim = openwns.simulator.getSimulator()
sim.outputStrategy = openwns.simulator.OutputStrategy.DELETE

#lte.support.helper.setupPhy(sim, Config.plmName, "InH")

# Use this to modify your logger levels
#import openwns.logger
#a = openwns.logger.globalRegistry

#a.setAttribute("LTE.UE3.L2.RLC", "level", 3)
#a.dump()


