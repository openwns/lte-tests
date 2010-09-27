import openwns.wrowser.simdb.api as api

bandwidth = 20.0e6

def filter(allscen):
    s = []

    # Loop over all scenarios
    # Check "fullPLCompensation" in parameterSet.params of each scenario if it is True
    # append the scenario to s if it fullfills the condition     

    return s

# Get the campaign by using the campaign name

# Use the campaign you previously got to retreive a list of all scenarios. Store this in an object calles "allscen"

from pylab import *
from cseReference import refs

cdfs = {}
cdfs["THRPT_incoming"] = []
cdfs["THRPT_aggregated"] = []

legends = {}
legends["incoming"] = []
legends["aggregated"] = []

direction = ["incoming", "aggregated"]

for d in direction: 
    name = "lte.total.window.%s.bitThroughput_UT_PDF" % d
    print "Reading %s" % name

    # Go to the top and implement the filter method. For the start you might just want to return all scenarios
    cdf = api.getCDFs(name, campaign, forScenarios = filter(allscen), agg="AVG")

    cdfs["THRPT_%s"%d].append(cdf)
    legends[d].append("openWNS")

# If you did everything right the lines below will plot you graph together with the reference graphs    
for cdf in cdfs["THRPT_incoming"]:
    for x,y in cdf:
        plot(array(x)/bandwidth,array(y))

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

for cdf in cdfs["THRPT_aggregated"]:
    for x,y in cdf:
        plot(array(x)/bandwidth,array(y))

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
