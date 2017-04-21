
import re
import os

#fileList = 'all_file.csv'
fileList = 'refine.csv'


def GetTputFromLog(f):
    Mbits_sum_re = re.compile(r".*SUM.*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Mbits/sec")
    Gbits_sum_re = re.compile(r".*SUM.*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Gbits/sec")

    Mbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Mbits/sec")
    Gbits_re = re.compile(r".*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Gbits/sec")

    line = f.readlines()[-1]
#        print line
    match = Mbits_sum_re.match(line)
    if match!=None:
        t1 = float(match.group("t1"))
        t2 = float(match.group("t2"))
        if t2-t1!=1:
            return float(match.group("value"))

    match = Gbits_sum_re.match(line)
    if match!=None:
        t1 = float(match.group("t1"))
        t2 = float(match.group("t2"))
        if t2-t1!=1:
            return float(match.group("value"))*1000

    match = Mbits_re.match(line)
    if match!=None:
        t1 = float(match.group("t1"))
        t2 = float(match.group("t2"))
        if t2-t1!=1:
            return float(match.group("value"))

    match = Gbits_re.match(line)
    if match!=None:
        t1 = float(match.group("t1"))
        t2 = float(match.group("t2"))
        if t2-t1!=1:
            return float(match.group("value"))*1000


def GetTput(tput_file):
    tput = '-'
    if not os.path.exists(tput_file):
        return tput
    with open(tput_file, 'r') as f:
        if tput_file.endswith('total_iperf.log'):
            tput = int(float(f.readlines()[0]))
        else:
	    tput = int(GetTputFromLog(f))

    f.close()
    return tput
def GetRTT(rtt_file):
    percentile = re.compile(r"sockperf: ---> percentile (?P<percent>.*) =\s+(?P<value>\S+)")
    rtt50 = '-'
    rtt999 = '-'
    if not os.path.exists(rtt_file):
        return ('-', '-')
    with open(rtt_file, 'r') as f:
        for line in f:
            match = percentile.match(line)
	    if match != None:
	        if match.group("percent") == "99.900":
	            rtt999 = int(float(match.group("value")))
	        if match.group("percent") == "50.000":
	            rtt50 = int(float(match.group("value")))
    f.close()
    return (rtt50, rtt999)

    
with open(fileList, 'r') as f:
    for line in f:
        line = line.strip()
        fields = line.split(',')
	[numReceiver, numFlow, rate, totalRate, tput_file, rtt_file] = fields
	tput = GetTput(tput_file)
	(rtt50, rtt999) = GetRTT(rtt_file)
	saturation = '-' if tput=='-' else tput/float(totalRate)/1000*100 if totalRate != '-' else tput/10000
	print ','.join(fields[:4]+ [ str((tput)), str(saturation), str((rtt50)), str((rtt999)) ])
	    
