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

numRun=9
numFlow=8

MbpsMatch = re.compile(r'.*Bytes\s*(?P<tput>\S+)\s*Mbits/sec')

def Config():
    print "============ configurations ================="
    print "default configuration file: %s" % mpl.matplotlib_fname()
    print "default font size: %s" % mpl.rcParams['font.size']
    print "legend fontsize: %s" % mpl.rcParams['legend.fontsize']
    print "============ configurations ================="


def GetData():
    tput = []
    for i in range(1, numRun+1):
        flows = []
	for j in range(1, numFlow+1):
	    fileName = ('run%d/iperf%d.log' % (i, j))
	    f = open(fileName, 'r')
	    lastLine = f.readlines()[-1]
	    match = MbpsMatch.match(lastLine)
	    if match==None:
	        print 'unmatched: ', lastLine
            else:
	        tput1= float( match.group("tput"))
		flows.append(tput1)
	tput.append(flows)
    return tput

def GetPlotData(data):
    means = []
    ses = []
    fis = []
    for flows in data:
        sum_x = sum(flows)
	sum_x2 = sum([i*i for i in flows])
	n = len(flows)
        # get average
        mean = sum_x/n
	# get std error
        err = sum_x2 / n - mean*mean
	se =  err ** 0.5
	# get faireness index
	fi =  (sum_x**2) / (n * sum_x2)

	means.append(mean)
	ses.append(se)
	fis.append(fi)
    #print (means, ses, fis)
    return (means, ses, fis)
	
def Plot(plotData):
    figName = 'figure.pdf'
    (means, ses, fis) = plotData
    n = len(means)
    index = range(1, n+1)
    width = 0.5
    xtick_labels = [ 'exp%d\n%.4f' % (i, fis[i-1]) for i in index]
    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    rects = ax.bar(index, means, width, yerr=ses, capsize=4)


    ax.set_ylabel('Mean Throughput (Mbps)')
    ax.set_xticks(index)
    ax.set_xticklabels(xtick_labels)

    fig.tight_layout()
    pp= PdfPages(figName)
    pp.savefig()
    pp.close()



def main():
    Config()
    data = GetData()
    plotData = GetPlotData(data)
    Plot(plotData)

if __name__=='__main__':
    main()
