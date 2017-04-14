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


FIGSIZE = (4, 3)

MARKERS = ['o','v','^','s','*','+','x']
COLORS = ["k", "c", "g", "b", "m", "r", "y"]
PATTERNS = ['ko','cv','g^','bs','m*','r+','yx']
LINEPATTERNS = ['ko-','cv-','g^-','bs-','m*-','r+-','yx-']




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
          



def PlotLatencyCDF():
    data_files = [
    'sockperf-2000-10000.log',
    'sockperf-2000-20000.log',
    'sockperf-2000-40000.log',
    'sockperf-2000-60000.log',
    'sockperf-2000-80000.log',
    'sockperf-2000-100000.log'
    ]
    legends = [
    '10KB',
    '20KB',
#    '30K',
    '40KB',
#    '50K',
    '60KB',
#    '70K',
    '80KB',
#    '90K',
    '100KB',
    ]
    figName='figure1.pdf'
    # get data (samples, percentiles)
    #(percentiles, samples) = GetCDFData("100KB_sockperf.log")
    #print percentiles
    #print samples
    # plot 
    plt.figure(figsize= FIGSIZE)
    ax = plt.subplot(1,1,1)
    patterns = []
    i = 0
    for data_file in data_files:
        (percentiles, samples) = GetCDFData(data_file)
#        print  percentiles, samples, i
        plt.plot( samples[0], samples[1], color=COLORS[i] )
        p = plt.plot( percentiles[0], percentiles[1], PATTERNS[i], label=legends[i], mec=COLORS[i] )
        patterns.append(p)
        i += 1
    ax.set_xscale('log')
    ax.set_xlim(10, 10000)
    ax.set_ylim(0, 1)
    ax.set_xlabel("RTT (us)")
    ax.set_ylabel("CDF")
    ax.yaxis.grid(True)
    plt.legend( bbox_to_anchor=(0.02, 0.98), ncol=1, loc='upper left', scatterpoints=2)
    plt.tight_layout()
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()

def PlotTput():
    data_files = [
    'iperf-2000-10000.txt',
    'iperf-2000-20000.txt',
    'iperf-2000-40000.txt',
    'iperf-2000-60000.txt',
    'iperf-2000-80000.txt',
    'iperf-2000-100000.txt'
    ]
    legends = [
    '10K',
    '20K',
#    '30K',
    '40K',
#    '50K',
    '60K',
#    '70K',
    '80K',
#    '90K',
    '100K',
    ]
    figName='figure2.pdf'
    plt.figure(figsize = FIGSIZE)
    ax = plt.subplot(1,1,1)
    patterns = []
    i = 0
    for data_file in data_files:
        tput = GetTputData(data_file)
	p = plt.plot(tput[0], tput[1], LINEPATTERNS[i], label=legends[i])
	patterns.append(p)
	i+=1
    plt.legend( bbox_to_anchor=(0.02, 0.98), ncol=3, loc='upper left', scatterpoints=2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Throughput (Mbit/s)")
    ax.set_ylim(0, 3000)
    plt.tight_layout()
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()
    


def main():
    ShowAndConfigParam()
    PlotLatencyCDF()
    PlotTput()

if __name__=='__main__':
    main()
