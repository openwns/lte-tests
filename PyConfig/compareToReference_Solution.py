import openwns.wrowser.simdb.api as api

bandwidth = 20.0e6

def filter(allscen):
    s = []
    
    for scen in allscen:
        # Check if the bool parameter "fullPLCompensation" is True
        if scen.parameterSet.params["fullPLCompensation"] == True:
            # Print the included parameter set and append to list
            print scen.parameterSet.params
            s.append(scen)	    
    return s

# get the campaign "TheName"
campaign = api.getCampaignByTitle("TheName")

# Get all scenarios of the campaign (each parameter set is one scenario)
allscen = api.getScenariosForCampaign(campaign)

# Used for plotting
from pylab import *

# Get the reference results from the file sceReference
from cseReference import refs

# Dict holding the resulting CDFs for DL and UL
cdfs = {}
cdfs["THRPT_incoming"] = []
cdfs["THRPT_aggregated"] = []

# Dict holding the legends for DL and UL
legends = {}
legends["incoming"] = []
legends["aggregated"] = []

# DL and UL
direction = ["incoming", "aggregated"]

# Do this for DL and UL
for d in direction: 
    # Look for this probe
    name = "lte.total.window.%s.bitThroughput_UT_PDF" % d
    print "Reading %s" % name

    # Get the CDF for this probe but only for scnearios returned by "filter", aggregate the results.
    cdf = api.getCDFs(name, campaign, forScenarios = filter(allscen), agg="AVG")

    # Insert the result in the dictonary and add a legend
    cdfs["THRPT_%s"%d].append(cdf)
    legends[d].append("openWNS")

# Plot the DL result    
for cdf in cdfs["THRPT_incoming"]:
    for x,y in cdf:
        plot(array(x)/bandwidth,array(y))

# Plot DL reference results
plot(refs["DL"]["InH"]["Org1"][0], refs["DL"]["InH"]["Org1"][1])
plot(refs["DL"]["InH"]["Org4"][0], refs["DL"]["InH"]["Org4"][1])
plot(refs["DL"]["InH"]["Org5"][0], refs["DL"]["InH"]["Org5"][1])
xlim(0.0, 1.0)
grid()
title("Normalized User Throughput InH Downlink")
legend(legends["incoming"] + ["Org1", "Org4", "Org5"], loc=4)
xlabel("User Throughput [bps/Hz]")
ylabel("P(X < x)")

figure()

# Plot UL results
for cdf in cdfs["THRPT_aggregated"]:
    for x,y in cdf:
        plot(array(x)/bandwidth,array(y))

# Plot UL reference results
plot(refs["UL"]["InH"]["Org1"][0], refs["UL"]["InH"]["Org1"][1])
plot(refs["UL"]["InH"]["Org5"][0], refs["UL"]["InH"]["Org5"][1])
xlim(0.0, 1.0)
grid()
title("Normalized User Throughput InH Uplink")
legend(legends["aggregated"] + ["Org1", "Org5"],loc=4)
xlabel("User Throughput [bps/Hz]")
ylabel("P(X < x)")
show()
clf()
