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

from scenarios.ituM2135.antenna import IndoorHotspotAntennaCreator
from scenarios.builders.creatorplacer import CreatorPlacerBuilder
import scenarios.channelmodel.channelmodelcreator
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

    cellRadius = 50
    distance = 25

    # Increase to at 15E6 for calibration
    dlTrafficRate = 0.0
    ulTrafficRate = 15E6

    # Increase to 20 for calibration
    nodes = 10

    # Use different seeds for calibration
    seed = 7

    if dlTrafficRate > 0.0:
        dlTraffic = scenarios.traffic.CBR(offset=0.0,
                                      trafficRate=trafficRate,
                                      packetSize = packetSize*8,
                                      )
    else:
        dlTraffic = None

    settlingTime = 1.05
    maxSimTime = 2.01

random.seed(Config.seed)

bsCreator = BSCreator(Config)
ueCreator = UECreator(Config)
bsPlacer = scenarios.placer.LinearPlacer(numberOfNodes = 2,
                                         positionsList = [Config.cellRadius, Config.cellRadius + Config.distance])
uePlacer = scenarios.placer.circular.CircularAreaPlacer(Config.nodes, Config.cellRadius, 3.0)
bsAntenna = scenarios.antenna.IsotropicAntennaCreator([0.0, 0.0, 5.0])

channelmodelcreator = scenarios.channelmodel.InHNLoSChannelModelCreator()
scenario = scenarios.builders.CreatorPlacerBuilder(bsCreator, bsPlacer, bsAntenna, ueCreator, uePlacer, channelmodelcreator)

import openwns.simulator

sim = openwns.simulator.getSimulator()
sim.outputStrategy = openwns.simulator.OutputStrategy.DELETE
sim.maxSimTime = Config.maxSimTime

sim.rng.seed = Config.seed
# end example

rang = openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "RANG")[0]

if Config.ulTrafficRate > 0.0:
    for ue in openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "UE"):

        binding = constanze.node.UDPClientBinding(ue.nl.domainName,
                                                  rang.nl.domainName,
                                                  777,
                                                  parentLogger=ue.logger,
                                                  qosClass=openwns.qos.undefinedQosClass)

        ulTraffic = constanze.traffic.CBR(offset=Config.startTrafficOffset,
                                          throughput=Config.ulTrafficRate,
                                          packetSize = Config.packetSize * 8)
        ue.addTraffic(binding, ulTraffic)

# DHCP, ARP, DNS for IP
ip.BackboneHelpers.createIPInfrastructure(sim, "LTERAN")

lte.support.helper.setupULScheduler(sim, "Fixed", Config.modes)

import lte.evaluation.default
eNBNodes = sim.simulationModel.getNodesByProperty("Type", "eNB")
ueNodes = sim.simulationModel.getNodesByProperty("Type", "UE")

for bs in eNBNodes:
    for ut in sim.simulationModel.getNodesByProperty("BS", bs):
        ut.dll.associateTo(bs.dll.address)
    

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


