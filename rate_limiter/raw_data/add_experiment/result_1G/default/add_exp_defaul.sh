#!/bin/sh

# Smaller byte queue limits : 1879048192 Bytes
for i in $(seq 0 39)
do
echo 1879048192 > /sys/class/net/enp6s0f0/queues/tx-$i/byte_queue_limits/limit_max
done


#TCP Small Queues : 256kB
echo 262144 > /proc/sys/net/ipv4/tcp_limit_output_bytes


sudo tc qdisc del dev enp6s0f0 root
sudo tc qdisc add dev enp6s0f0 root handle 1: htb default 1
sudo tc class add dev enp6s0f0 parent 1:0 classid 1:1 htb rate 1000mbit

cd /users/wenfeiwu/add_experi/default
iperf -c 10.10.1.1 -t 20 -i 1 > iperf.txt &
(sleep 5s
sockperf pp -i 10.10.1.1 -t 10 -p 8899 --tcp --pps=100 --full-log sockperf-$i-$j.log)
sleep 3s
