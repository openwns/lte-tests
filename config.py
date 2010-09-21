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
from scenarios.traffic import VoIP

import constanze.node
from lte.creators.fdd import BSCreator, UECreator
import lte.support.helper
import openwns.qos

ueOffset = 0.05 
duration = 1.0

class Config:
    modes = ["ltefdd10"]
    useTCP = False
    dlTraffic = VoIP(offset=0.0)
    settlingTime = 1.05
    maxSimTime = 2.1

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
sim.maxSimTime = Config.maxSimTime

rang = openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "RANG")[0]

for ue in openwns.simulator.getSimulator().simulationModel.getNodesByProperty("Type", "UE"):
    ue.addTraffic(constanze.node.UDPClientBinding(ue.nl.domainName,
                                                  rang.nl.domainName,
                                                  777,
                                                  parentLogger=ue.logger,
                                                  qosClass=openwns.qos.undefinedQosClass,
                                                  nodeInCenterCell=True),
                  constanze.traffic.VoIP(offset=ueOffset))

from ip.VirtualARP import VirtualARPServer
from ip.VirtualDHCP import VirtualDHCPServer
from ip.VirtualDNS import VirtualDNSServer

varp = VirtualARPServer("vARP", "LTERAN")
sim.simulationModel.nodes.append(varp)
vdhcp = VirtualDHCPServer("vDHCP@",
                          "LTERAN",
                          "192.168.0.2", "192.168.254.253",
                          "255.255.0.0")

sim.simulationModel.nodes.append(vdhcp)

vdns = VirtualDNSServer("vDNS", "ip.DEFAULT.GLOBAL")
sim.simulationModel.nodes.append(vdns)

#lte.support.helper.setupPhy(sim, Config.plmName, "InH")

import lte.evaluation.default
eNBNodes = sim.simulationModel.getNodesByProperty("Type", "eNB")
ueNodes = sim.simulationModel.getNodesByProperty("Type", "UE")
eNBIDs = [node.nodeID for node in eNBNodes]
ueIDs = [node.nodeID for node in ueNodes]
lte.evaluation.default.installEvaluation(sim,
                                         eNBIDs + ueIDs,
                                         eNBIDs,
                                         ueIDs,
                                         Config.settlingTime)

# Use this to modify your logger levels
#import openwns.logger
#a = openwns.logger.globalRegistry

#a.setAttribute("LTE.UE3.L2.RLC", "level", 3)
#a.dump()


