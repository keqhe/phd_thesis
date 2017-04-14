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



def PlotDiffFlows():
    latency_files = [
      [ 
         '1000mbps/8iperfs/limiter1/sockperf1000mbps8iperfs.log',
         '2000mbps/8iperfs/limiter1/sockperf2000mbps8iperfs.log',
         '3000mbps/8iperfs/limiter1/sockperf3000mbps8iperfs.log',
         '4000mbps/8iperfs/limiter1/sockperf4000mbps8iperfs.log',
         '5000mbps/8iperfs/limiter1/sockperf5000mbps8iperfs.log',
      ],
      [ 
         '1000mbps/8iperfs/limiter2/sockperf1000mbps8iperfs.log',
         '2000mbps/8iperfs/limiter2/sockperf2000mbps8iperfs.log',
         '3000mbps/8iperfs/limiter2/sockperf3000mbps8iperfs.log',
         '4000mbps/8iperfs/limiter2/sockperf4000mbps8iperfs.log',
         '5000mbps/8iperfs/limiter2/sockperf5000mbps8iperfs.log',
      ],
      [ 
         '1000mbps/16iperfs/limiter1/sockperf1000mbps16iperfs.log',
         '2000mbps/16iperfs/limiter1/sockperf2000mbps16iperfs.log',
         '3000mbps/16iperfs/limiter1/sockperf3000mbps16iperfs.log',
         '4000mbps/16iperfs/limiter1/sockperf4000mbps16iperfs.log',
         '5000mbps/16iperfs/limiter1/sockperf5000mbps16iperfs.log',
      ],
      [ 
         '1000mbps/16iperfs/limiter2/sockperf1000mbps16iperfs.log',
         '2000mbps/16iperfs/limiter2/sockperf2000mbps16iperfs.log',
         '3000mbps/16iperfs/limiter2/sockperf3000mbps16iperfs.log',
         '4000mbps/16iperfs/limiter2/sockperf4000mbps16iperfs.log',
         '5000mbps/16iperfs/limiter2/sockperf5000mbps16iperfs.log',
      ],
    ]
    legends =   [ '1Gbps', '2Gbps', '3Gbps', '4Gbps', '5Gbps' ]
    figName=FIGNAME
    fig = plt.figure(figsize=(8, 6))

    # latency CDF
    pos = [221, 222, 223, 224]
    xlabels = ["RTT(us) of Rate Limter 1 (8 iperfs)","RTT(us) of Rate Limiter 2 (8 iperfs)", "RTT(us) of Rate Limter 1 (16 iperfs)","RTT(us) of Rate Limiter 2 (16 iperfs)"]
    patterns = []
    for idx in (0, 1, 2, 3):
        patterns = []
        ax = plt.subplot(pos[idx])
        for i in range(len(latency_files[idx])):
            f = latency_files[idx][i]
            (percentiles, samples) = GetCDFData(f)
            plt.plot(samples[0], samples[1], color=COLORS[i])
            p, = plt.plot( percentiles[0], percentiles[1], PATTERNS[i], label=legends[i], mec=COLORS[i])
            patterns.append(p)
        ax.set_xscale('log')
        ax.set_xlabel(xlabels[idx])
        ax.set_ylabel('CDF')
        ax.yaxis.grid(True, linestyle='--')
	ax.set_xlim(1000, 10000)
    plt.figlegend(patterns, legends, loc='upper center', ncol=len(patterns))

    plt.tight_layout(rect=(0, 0, 1, 0.92))
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()




def Plot():
    PlotDiffFlows()

if __name__ == '__main__':
    Plot()
