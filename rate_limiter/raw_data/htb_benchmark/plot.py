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



def Plot(figName, legends, rtt_files, xlabels):
    plt.figure(figsize=(12, 2.5))

    patterns = []
    pos = [141, 142, 143, 144]
    for idx  in range(4):
        ax = plt.subplot(pos[idx])
        for i in range(len(rtt_files[idx])):
            f = rtt_files[idx][i]
            (percentiles, samples) = GetCDFData(f)
            plt.plot(samples[0], samples[1], color=COLORS[i])
            p = plt.plot( percentiles[0], percentiles[1], PATTERNS[i], label=legends[i], mec=COLORS[i])
            patterns.append(p)
        ax.set_xscale('log')
        ax.set_xlabel(xlabels[idx])
        ax.set_ylabel('CDF')
        ax.yaxis.grid(True, linestyle='--')
        ax.set_xlim(10, 10000)
    plt.legend(bbox_to_anchor=(-1.5, 0.98), ncol=len(patterns), loc='lower center', framealpha = 1)
    plt.tight_layout(rect=(0,0, 1, 0.95))
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()


if __name__ == '__main__':
    rtt_files = [
    ['1ratelimiter/2iperfs/sockperf_noiperf.log',
        '1ratelimiter/1iperf/sockperf1G.log',
        '1ratelimiter/1iperf/sockperf2G.log',
        '1ratelimiter/1iperf/sockperf4G.log',
        '1ratelimiter/1iperf/sockperf8G.log'
    ], 
    ['1ratelimiter/2iperfs/sockperf_noiperf.log',
        '1ratelimiter/2iperfs/sockperf1G.log',
        '1ratelimiter/2iperfs/sockperf2G.log',
        '1ratelimiter/2iperfs/sockperf4G.log',
        '1ratelimiter/2iperfs/sockperf8G.log'
    ], 
    ['1ratelimiter/2iperfs/sockperf_noiperf.log',
        '1ratelimiter/8_16_iperfs/1000mbps/8iperfs/sockperf1000mbps8iperfs.log',
        '1ratelimiter/8_16_iperfs/2000mbps/8iperfs/sockperf2000mbps8iperfs.log',
        '1ratelimiter/8_16_iperfs/4000mbps/8iperfs/sockperf4000mbps8iperfs.log',
        '1ratelimiter/8_16_iperfs/8000mbps/8iperfs/sockperf8000mbps8iperfs.log'
    ], 
    ['1ratelimiter/2iperfs/sockperf_noiperf.log',
        '1ratelimiter/8_16_iperfs/1000mbps/16iperfs/sockperf1000mbps16iperfs.log',
        '1ratelimiter/8_16_iperfs/2000mbps/16iperfs/sockperf2000mbps16iperfs.log',
        '1ratelimiter/8_16_iperfs/4000mbps/16iperfs/sockperf4000mbps16iperfs.log',
        '1ratelimiter/8_16_iperfs/8000mbps/16iperfs/sockperf8000mbps16iperfs.log'
    ]] 
    figName = 'one_receiver.pdf'
    legends = ['no config', '1Gbps', '2Gbps', '4Gbps', '8Gbps']
    xlabels = [ 'RTT (us) with 1 bg flow', 'RTT (us) with 2 bg flows', 'RTT (us) with 8 bg flows', 'RTT (us) with 16 bg flows' ]
    Plot(figName, legends, rtt_files, xlabels)
    rtt_files = [
    ['2ratelimiters/1iperf/sockperf1_baseline.log',
        '2ratelimiters/1iperf/sockperf1_2G.log',
        '2ratelimiters/1iperf/sockperf1_3G.log',
        '2ratelimiters/1iperf/sockperf1_4G.log',
        '2ratelimiters/1iperf/sockperf1_5G.log'
    ], 
    ['2ratelimiters/1iperf/sockperf1_baseline.log',
        '2ratelimiters/2iperfs/skpf1_2G.log',
        '2ratelimiters/2iperfs/skpf1_3G.log',
        '2ratelimiters/2iperfs/skpf1_4G.log',
        '2ratelimiters/2iperfs/skpf1_5G.log'
    ], 
    ['2ratelimiters/1iperf/sockperf1_baseline.log',
        '2ratelimiters/8_16_iperfs/2000mbps/8iperfs/limiter1/sockperf2000mbps8iperfs.log',
        '2ratelimiters/8_16_iperfs/3000mbps/8iperfs/limiter1/sockperf3000mbps8iperfs.log',
        '2ratelimiters/8_16_iperfs/4000mbps/8iperfs/limiter1/sockperf4000mbps8iperfs.log',
        '2ratelimiters/8_16_iperfs/5000mbps/8iperfs/limiter1/sockperf5000mbps8iperfs.log',
    ], 
    ['2ratelimiters/1iperf/sockperf1_baseline.log',
        '2ratelimiters/8_16_iperfs/2000mbps/16iperfs/limiter1/sockperf2000mbps16iperfs.log',
        '2ratelimiters/8_16_iperfs/3000mbps/16iperfs/limiter1/sockperf3000mbps16iperfs.log',
        '2ratelimiters/8_16_iperfs/4000mbps/16iperfs/limiter1/sockperf4000mbps16iperfs.log',
        '2ratelimiters/8_16_iperfs/5000mbps/16iperfs/limiter1/sockperf5000mbps16iperfs.log',
    ]] 
    figName = 'two_receivers.pdf'
    legends = ['no config', '2Gbps', '3Gbps', '4Gbps', '5Gbps']
    Plot(figName, legends, rtt_files, xlabels)
