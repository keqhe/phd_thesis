import re

def GetTputData(fileName): # total
    Mbits_re = re.compile(r".*SUM.*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Mbits/sec")
    Gbits_re = re.compile(r".*SUM.*\s+(?P<t1>\S+)-\s*(?P<t2>\S+)\s+sec.*\s+(?P<value>\S+)\s*Gbits/sec")
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

suffix = [ '2G', '3G', '4G', '5G']

files = [ ]

for s in suffix:
    f1 = 'iperf1_%s.txt' % s
    f2 = 'iperf2_%s.txt' % s
    f3 = '%s_total_iperf.log' % s
    files.append((f1, f2, f3))


for (f1, f2, f3) in files:
    tput1 = GetTputData(f1) 
    tput2 = GetTputData(f2)
    total = tput1+tput2
    print total
    with open(f3, 'w') as f:
        f.write( str(total) )
    f.close()

