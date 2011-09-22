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
    modes = ["ltefdd5"]
    useTCP = False
    useApp = True

    # Increase for real results
    nodes = 2

    # Use different seeds for real results
    seed = 1

    # Change uplink power control parameter (alpha = 1 => full pathloss compensation)
    # Specifications allow values [0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    alpha = 0.0

    # Should be increased if alpha is below zero. 
    # Specifications allow values from -126dBm to +23dBm
    pNull = "4 dBm"

    # Set to 21.15 for real results
    settlingTime = 1.05
    maxSimTime = 2.05

# begin example "lte.tutorial.experiment1.prnd"
random.seed(Config.seed)
# end example

# begin example "lte.tutorial.experiment1.scenario"
bsCreator = BSCreator(Config)
ueCreator = UECreator(Config)

scenario = scenarios.ituM2135.CreatorPlacerBuilderIndoorHotspot(
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


# DHCP, ARP, DNS for IP
ip.BackboneHelpers.createIPInfrastructure(sim, "LTERAN")

# begin example "lte.tutorial.experiment1.APC"
lte.support.helper.setupUL_APC(sim, Config.modes, alpha = Config.alpha, pNull = Config.pNull)
#end example

# begin example "lte.tutorial.experiment1.ft"
#lte.support.helper.setupFTFading(sim, "InH", Config.modes)
# end example


# Client will try to establish the session between [0..SettlingTime / 3]
lte.support.helper.createULVoIPTraffic(sim, settlingTime = Config.settlingTime, 
    maxStartDelay = float(Config.settlingTime) / 3.0, probeEndTime = Config.maxSimTime - 0.1)
# Server will try to establish the session between [SettlingTime / 3.. SettlingTime * 2 / 3].
# Client will not start before first PDU from server is received
lte.support.helper.createDLVoIPTraffic(sim, settlingTime = Config.settlingTime,
    trafficStartDelay = float(Config.settlingTime) / 3.0, probeEndTime = Config.maxSimTime - 0.1)
# This assures all connections can be established before actual VoIP traffic starts
# Check the application.connectionEstablished probe. It must have mean 1.0 if everything
# is OK: L2 connection established; Server session created after first PDU from client 
# was received; client received at least one PDU from server.

lte.support.helper.setupULScheduler(sim, "PersistentVoIP", Config.modes)
lte.support.helper.disablePhyUnicastULTransmission(sim, Config.modes)

#lte.support.helper.setHARQRetransmissionLimit(sim, Config.modes, 20)

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

import applications.evaluation.default
applications.evaluation.default.installEvaluation(sim, eNBIDs, ueIDs,
                                                ['VoIP'], Config.settlingTime)

from openwns.evaluation import *
sourceName = 'scheduler.persistentvoip.FrameOccupationFairness'
node = openwns.evaluation.createSourceNode(sim, sourceName)
node.getLeafs().appendChildren(SettlingTimeGuard(settlingTime = Config.settlingTime))
node.getLeafs().appendChildren(Accept(by='nodeID', ifIn = eNBIDs + ueIDs, suffix='CenterCell'))
node.getLeafs().appendChildren(PDF(name = sourceName,
                                 description = 'Frame Occupation Fairness',
                                 minXValue = 0,
                                 maxXValue = 1,
                                 resolution = 100))

import openwns.evaluation.default

openwns.evaluation.default.installEvaluation(openwns.simulator.getSimulator())
openwns.simulator.getSimulator().statusWriteInterval = 10 # in seconds realTime
