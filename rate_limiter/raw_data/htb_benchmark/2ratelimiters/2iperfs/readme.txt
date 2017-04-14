#this folder contains all data of two parallel iperf flow and two rate limiters,
#"iperf*" is bandwidth of the link, "skpf*" is the data measured by sockperf. 

####################################################
###################  10-19 update  #################
This folder contains data of two figures witch titled "RTT-CDF by two rate limiters and two parallel iperf flow". xlabel is "RTT", ylabel is "CDF". xrange is 0:4000,xitcs is 1000. yrange is 0:100, ytics is 10. The key is "min=xG".
first firgure is drawed from skpt1_2G.log to skpt1_5G.log(sockperf1_baseline.log included).
second firgure is drawed from skpt2_2G.log to skpt2_5G.log(sockperf2_baseline.log included).
