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
import scenarios.traffic

#from openwns.wrowser.simdb.SimConfig import params

import constanze.node
from lte.creators.fdd import BSCreator, UECreator
import lte.support.helper
import openwns.qos

import ip.BackboneHelpers

import random

class Config:
    modes = ["ltefdd20"]
    useTCP = False
    packetSize = 1500
    startTrafficOffset = 0.05 # startTime

    # Increase to at 15E6 for calibration
    trafficRate = 1E5

    # Increase to 20 for calibration
    nodes = 2

    # Use different seeds for calibration
    seed = 7

    # Change uplink power control parameter (alpha = 1 => full pathloss compensation)
    # Specifications allow values [0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    alpha = 1.0

    # Should be increased if alpha is below zero. 
    # Specifications allow values from -126dBm to +23dBm
    pNull = "-106 dBm"

    dlTraffic = scenarios.traffic.CBR(offset=0.0,
                                      trafficRate=trafficRate,
                                      packetSize = packetSize*8,
                                      )

    settlingTime = 1.05
    maxSimTime = 2.01

# begin example "lte.tutorial.experiment1.prnd"
random.seed(Config.seed)
# end example

# begin example "lte.tutorial.experiment1.scenario"
bsCreator = BSCreator(Config)
ueCreator = UECreator(Config)

scenario = scenarios.builders.CreatorPlacerBuilderIndoorHotspot(
    bsCreator, 
    ueCreator, 
    numberOfNodes = Config.nodes)
#end example

# begin example "lte.tutorial.experiment1.config"
import openwns.simulator

sim = openwns.simulator.getSimulator()
sim.outputStrategy = openwns.simulator.OutputStrategy.DELETE
sim.maxSimTime = Config.maxSimTime

sim.rng.seed = Config.seed
# end example

rang = openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "RANG")[0]

for ue in openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "UE"):

    binding = constanze.node.UDPClientBinding(ue.nl.domainName,
                                              rang.nl.domainName,
                                              777,
                                              parentLogger=ue.logger,
                                              qosClass=openwns.qos.undefinedQosClass)

    ulTraffic = constanze.traffic.CBR(offset=Config.startTrafficOffset,
                                      throughput=Config.trafficRate,
                                      packetSize = Config.packetSize * 8)
    ue.addTraffic(binding, ulTraffic)

# DHCP, ARP, DNS for IP
ip.BackboneHelpers.createIPInfrastructure(sim, "LTERAN")

# begin example "lte.tutorial.experiment1.APC"
lte.support.helper.setupUL_APC(sim, Config.modes, alpha = Config.alpha, pNull = Config.pNull)
#end example

# begin example "lte.tutorial.experiment1.ft"
lte.support.helper.setupFTFading(sim, "InH", Config.modes)
# end example

import lte.evaluation.default
eNBNodes = sim.simulationModel.getNodesByProperty("Type", "eNB")
ueNodes = sim.simulationModel.getNodesByProperty("Type", "UE")
eNBIDs = [node.nodeID for node in eNBNodes]
ueIDs = [node.nodeID for node in ueNodes]
lte.evaluation.default.installEvaluation(sim,
                                         eNBIDs + ueIDs,
                                         eNBIDs,
                                         ueIDs,
                                         Config.settlingTime,
                                         maxThroughputPerUE = 20.0e06)

# Use this to modify your logger levels
#import openwns.logger
#a = openwns.logger.globalRegistry

#a.setAttribute("LTE.UE3.L2.RLC", "level", 3)
#a.dump()


