#!/bin/sh


# Smaller byte queue limits : 256KB
for i in $(seq 0 39)
do
echo 262144 > /sys/class/net/enp6s0f0/queues/tx-$i/byte_queue_limits/limit_max
done


sudo tc qdisc del dev enp6s0f0 root
sudo tc qdisc add dev enp6s0f0 root handle 1: htb default 1
sudo tc class add dev enp6s0f0 parent 1:0 classid 1:1 htb rate 500mbit


cd /users/wenfeiwu/add_experi/BQL
#iperf -c 10.10.1.1 -p 5002 -t 20 -i 1 -D > iperf_background.txt
(iperf -c 10.10.1.1 -p 5001 -t 20 -i 1 > iperf.txt) &
(sleep 5s
sockperf pp -i 10.10.1.1 -t 10 -p 8899 --tcp --pps=100 --full-log sockperf500m.log)
sleep 3s
