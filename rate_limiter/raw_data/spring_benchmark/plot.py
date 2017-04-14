#!/usr/bin/python
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
import matplotlib.gridspec as gridspec

#import matplotlib
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

import re



MARKERS = ['v','^','s','*','+','x']
COLORS = [ "c", "g", "b", "m", "r", "y"]
PATTERNS = ['cv','g^','bs','m*','r+','yx']
LINEPATTERNS = ['cv-','g^-','bs-','m*-','r+-','yx-']

#MARKERS = ['o','v','^','s','*','+','x']
#COLORS = ["k", "c", "g", "b", "m", "r", "y"]
#PATTERNS = ['ko','cv','g^','bs','m*','r+','yx']
#LINEPATTERNS = ['ko-','cv-','g^-','bs-','m*-','r+-','yx-']



def ShowAndConfigParam():
    print "============ configurations ================="
    print "default configuration file: %s" % mpl.matplotlib_fname()
    print "default font size: %s" % mpl.rcParams['font.size']
    print "legend fontsize: %s" % mpl.rcParams['legend.fontsize']
    print "============ configurations ================="


def GetCDFData(fileName):
    percentile_re_1 = re.compile(r"sockperf: ---> <(?P<max_or_min>.*)> observation =\s+(?P<value>\S+)")
    percentile_re_2 = re.compile(r"sockperf: ---> percentile (?P<percent>.*) =\s+(?P<value>\S+)")
    sample_re = re.compile(r"(?P<snd>\d+.\d*), (?P<rcv>\d+.\d*)")
    percentiles = []
    samples = []
    f = open(fileName, 'r')
    for line in f.readlines():
        match = percentile_re_1.match(line)
        if match!= None:
            if match.group("max_or_min") == "MAX":
                percent = 1
            else:
                percent = 0
            percentiles.append( ( float(match.group("value")), percent) )
            continue
        match = percentile_re_2.match(line)
        if match!=None:
            percentiles.append( ( float(match.group("value")), float(match.group("percent"))/100 ) )
            continue
        match = sample_re.match(line)
        if match != None:
            latency = float(match.group("rcv")) - float(match.group("snd"))
            samples.append(latency*1000000)
    f.close()
    percentiles = [ [p[0]*2 for p in percentiles], [p[1] for p in percentiles]]
    samples.sort()
    samples = (samples,  [float(i)/len(samples) for i in range(len(samples))])
    return (percentiles, samples)

def GetTputData(fileName):
    Mbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Mbits/sec")
    Gbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Gbits/sec")
    tput = []
    f = open(fileName, 'r')
    for line in f.readlines():
        #print line
        match = Mbits_re.match(line)
        if match!=None:
            t1 = float(match.group("t1"))
            t2 = float(match.group("t2"))
            if t2-t1!=1:
                continue
            tput.append( (t2, float(match.group("value")) ) )
            continue
        match = Gbits_re.match(line)
        if match!=None:
            t1 = float(match.group("t1"))
            t2 = float(match.group("t2"))
            if t2-t1!=1:
                continue
            tput.append( (t2, float(match.group("value"))*1000 ) )
            continue
    tput = [[t[0] for t in tput], [t[1] for t in tput]]
    return tput
          

def Plot(figName, rtt_files, tput_files, legends, ylim):
    plt.figure(figsize=(6, 2.5))

    ax = plt.subplot(121)
    i = 0
    for f in rtt_files:
        (percentiles, samples) = GetCDFData(f)
	plt.plot(samples[0], samples[1], color=COLORS[i])
	plt.plot(percentiles[0], percentiles[1], PATTERNS[i], label=legends[i], mec=COLORS[i])
	i+=1
    
    ax.set_xscale('log')
    ax.set_xlim(10, 10000)
    ax.set_xlabel('RTT(us)')
    ax.set_ylabel('CDF')
    ax.yaxis.grid(True, linestyle='--')


    ax = plt.subplot(122)
    patterns = []
    i = 0
    for f in tput_files:
        tput = GetTputData(f)
	p = plt.plot(tput[0], tput[1], LINEPATTERNS[i], label=legends[i])
	patterns.append(p)
	i+=1
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Throughput (mbps)")
    ax.set_ylim(ylim)

    plt.legend(bbox_to_anchor=(-0.2,0.97), ncol=len(patterns), loc='lower center')
    plt.tight_layout(rect=(0,0,1,0.95))

    pp = PdfPages(figName)
    pp.savefig()
    pp.close()



def main():
    ShowAndConfigParam()
    figName='1gbps.pdf'
    tputFiles = [
    'timely1000mbps/alpha2048/beta2048/difference10000/iperf5000_15000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/iperf10000_20000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/iperf20000_30000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/iperf30000_40000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/iperf40000_50000.log',
    ]
    rttFiles = [
    'timely1000mbps/alpha2048/beta2048/difference10000/sockperf5000_15000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/sockperf10000_20000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/sockperf20000_30000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/sockperf30000_40000.log',
    'timely1000mbps/alpha2048/beta2048/difference10000/sockperf40000_50000.log',
    ]
    legends=['5KB', '10KB', '20KB', '30KB', '40KB']
    ylim=(0, 1200)
    Plot(figName, rttFiles, tputFiles, legends, ylim)


    figName='2gbps.pdf'
    tputFiles = [
    'timely2000mbps/alpha2048/beta2048/difference20000/iperf5000_25000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/iperf10000_30000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/iperf20000_40000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/iperf30000_50000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/iperf40000_60000.log',
    ]
    rttFiles = [
    'timely2000mbps/alpha2048/beta2048/difference20000/sockperf5000_25000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/sockperf10000_30000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/sockperf20000_40000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/sockperf30000_50000.log',
    'timely2000mbps/alpha2048/beta2048/difference20000/sockperf40000_60000.log',
    ]
    legends=['5KB', '10KB', '20KB', '30KB', '40KB']
    ylim=(0, 2400)
    Plot(figName, rttFiles, tputFiles, legends, ylim)




if __name__=='__main__':
    main()
