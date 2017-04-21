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

FIGNAME = 'figure.pdf'



def ShowAndConfigParam():
    print "============ configurations ================="
    print "default configuration file: %s" % mpl.matplotlib_fname()
    print "default font size: %s" % mpl.rcParams['font.size']
    print "legend fontsize: %s" % mpl.rcParams['legend.fontsize']
    print "============ configurations ================="



def GetCPUData(fileName):
    cpu_re = re.compile(r'.*(AM|PM)\s*all.*\s(?P<cpu>\S+)$')
    cpu = []
    f = open(fileName, 'r')
    for line in f.readlines():
        #print line
        match = cpu_re.match(line)
        if match!=None:
            t = 1-float(match.group("cpu"))/100
	    cpu.append(t)
    print cpu
    return cpu
          




def PlotCPU():
    data_files = [
    'rawhtb8iperf2Gbps_cpuoverhead.txt',
    'tcpece8iperf2Gbps_cpuoverhead.txt',
    'timely8iperf2Gbps_cpuoverhead.txt'
    ]
    legends = [
    'HTB',
    'DEM',
    'SPRING'
    ]
    figName=FIGNAME
    plt.figure(figsize = FIGSIZE)
    ax = plt.subplot(1,1,1)
    patterns = []
    i = 0
    for data_file in data_files:
        cpu = GetCPUData(data_file)
	xs = range(1, len(cpu)+1)
	p = plt.plot(xs, cpu, LINEPATTERNS[i], label=legends[i])
	patterns.append(p)
	i+=1
    #plt.legend( bbox_to_anchor=(0.02, 0.98), ncol=3, loc='upper left', scatterpoints=2)
    plt.legend(ncol=3, loc='upper left', scatterpoints=2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CPU Utilization")
    ax.set_ylim(0, 0.01)
    plt.tight_layout()
    pp = PdfPages(figName)
    pp.savefig()
    pp.close()
    


def main():
    ShowAndConfigParam()
    PlotCPU()

if __name__=='__main__':
    main()
