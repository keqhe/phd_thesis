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

#====================param================================
FIGSIZE = (4, 3)
FIGNAME='figure.pdf'

MARKERS = ['o','v','^','s','*','+','x']
COLORS = ["k", "c", "g", "b", "m", "r", "y"]
PATTERNS = ['ko','cv','g^','bs','m*','r+','yx']
LINEPATTERNS = ['ko-','cv-','g^-','bs-','m*-','r+-','yx-']
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




def PlotLatencyCDF():
    data_files = [
    'baseline.log',
    '1G.log',
    '2G.log',
    '4G.log',
    '6G.log',
    '8G.log',
    '10G.log'
    ]
    legends = [
    'no iperf',
    '1Gbps',
    '2Gbps',
    '4Gbps',
    '6Gbps',
    '8Gbps',
    '10Gbps'
    ]
    figName=FIGNAME
    plt.figure(figsize= FIGSIZE)
    ax = plt.subplot(1,1,1)
    patterns = []
    i = 0
    for data_file in data_files:
        (percentiles, samples) = GetCDFData(data_file)
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
    plt.legend( bbox_to_anchor=(0.02, 0.98), ncol=1, loc='upper left', scatterpoints=2, framealpha=1)
    plt.tight_layout()
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()



def Plot():
    ShowAndConfigParam()
    PlotLatencyCDF()

if __name__=='__main__':
    Plot()

