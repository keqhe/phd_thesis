import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
import matplotlib.gridspec as gridspec

#import matplotlib
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

import re
import os

#====================param================================
FIGSIZE = (8, 4)
FIGNAME='figure.pdf'
TPUT_YLIM = (0, 2000)
LATE_YLIM = (0, 500)

MARKERS = ['o','v','^','s','*','+','x']
COLORS = ["k", "c", "g", "b", "m", "r", "y"]
PATTERNS = ['ko','cv','g^','bs','m*','r+','yx']
LINEPATTERNS = ['ko-','cv-','g^-','bs-','m*-','r+-','yx--']
#====================param================================



def ShowAndConfigParam():
    mpl.rcParams['font.size']=14
    mpl.rcParams['legend.fontsize']='small'
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
            percentiles.append( ( float(match.group("value")), match.group("max_or_min") ) )
            continue
        match = percentile_re_2.match(line)
        if match!=None:
            percentiles.append( ( float(match.group("value")), match.group("percent") ) )
            continue
        match = sample_re.match(line)
        if match != None:
            latency = float(match.group("rcv")) - float(match.group("snd"))
            samples.append(latency*1000000)
    f.close()
    percentiles = {p[1]:(p[0]*2)  for p in percentiles}
    samples.sort()
    samples = (samples,  [float(i)/len(samples) for i in range(len(samples))])
    return percentiles
    #return (percentiles, samples)


def GetTputData(fileName): # total
    Mbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Mbits/sec")
    Gbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Gbits/sec")
    tput = []
    f = open(fileName, 'r')
    for line in f.readlines():
#        print line
        match = Mbits_re.match(line)
        if match!=None:
            t1 = float(match.group("t1"))
            t2 = float(match.group("t2"))
            if t2-t1!=1:
                return float(match.group("value"))
        match = Gbits_re.match(line)
        if match!=None:
#            print 'match Gbits'
            t1 = float(match.group("t1"))
            t2 = float(match.group("t2"))
            if t2-t1!=1:
                return float(match.group("value"))*1000

def GetThresholds():
    thresholds=[]
    for f in os.listdir('.'):
        if f.startswith('iperf'):
	    thresholds.append( int(f[5:].split('.')[0]) )
    return sorted(thresholds)
def Plot():
    thresholds = GetThresholds() #range(0, 30001, 1000)

    xs = [ t/1000 for t in thresholds]
    lines =[     [],    [],     [],     [],     [],     [],       []]
    legends =  [ 'MIN', '0.25', '0.5', '0.75', '0.99', '0.999', 'tput' ]

    for t in thresholds:
        sockfile = 'sockperf%d.log' % t
        percentiles = GetCDFData(sockfile)
        lines[0].append(percentiles['MIN'])
        lines[1].append(percentiles['25.000'])
        lines[2].append(percentiles['50.000'])
        lines[3].append(percentiles['75.000'])
        lines[4].append(percentiles['99.000'])
        lines[5].append(percentiles['99.900'])

	iperffile = 'iperf%d.log' % t
        tput = GetTputData(iperffile)
	lines[6].append(tput)
    figName=FIGNAME
    fig, ax = plt.subplots(figsize=FIGSIZE)
    patterns=[]
    for i in range(6):
        p, = ax.plot(xs, lines[i], LINEPATTERNS[i], label=legends[i])
	patterns.append(p)
    ax2 = ax.twinx()
    p, = ax2.plot(xs, lines[6], LINEPATTERNS[6], label=legends[6])
    patterns.append(p)

    ax.set_ylabel('RTT (us)')
    ax2.set_ylabel('Throughput (Mbps)') 
    ax2.set_ylim(TPUT_YLIM)
    ax.set_xlabel('Threshold (kB)')
    ax.set_ylim(LATE_YLIM)
    ax.yaxis.grid(True, linestyle='--')

    plt.legend(patterns, [l.get_label() for l in patterns], ncol=1, loc='upper left', framealpha=1)

    plt.tight_layout(rect=(0, 0, 1, 1))
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()





if __name__ == '__main__':
    Plot()
                                       
