#!/bin/sh


# Smaller byte queue limits : 256KB
for i in $(seq 0 39)
do
echo 262144 > /sys/class/net/enp6s0f0/queues/tx-$i/byte_queue_limits/limit_max
done


sudo tc qdisc del dev enp6s0f0 root
sudo tc qdisc add dev enp6s0f0 root handle 1: htb
sudo tc class add dev enp6s0f0 parent 1: classid 1:1 htb  rate 10000mbit prio 3
sudo tc class add dev enp6s0f0 parent 1:1 classid 1:2 htb rate 500mbit prio 0
sudo tc class add dev enp6s0f0 parent 1:1 classid 1:3 htb rate 500mbit prio 2

sudo iptables -A OUTPUT -t mangle -p tcp --dport 8899 -j MARK --set-mark 15
sudo tc filter add dev enp6s0f0 protocol ip parent 1:0 prio 0 handle 15 fw flowid 1:2


sudo iptables -A OUTPUT -t mangle -p tcp --dport 5001 -j MARK --set-mark 16
sudo tc filter add dev enp6s0f0 protocol ip parent 1:0 prio 2 handle 16 fw flowid 1:3





cd /users/wenfeiwu/add_experi/BQL_prio
#iperf -c 10.10.1.1 -p 5002 -t 20 -i 1 -D > iperf_background.txt
(iperf -c 10.10.1.1 -p 5001 -t 20 -i 1 > iperf.txt) &
(sleep 5s
sockperf pp -i 10.10.1.1 -t 10 -p 8899 --tcp --pps=100 --full-log sockperf500m.log)
sleep 3s
