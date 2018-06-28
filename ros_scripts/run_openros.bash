#!/bin/bash
sudo pkill -9 python 
pid=$!
wait $pid

cd /home/vagrant/openwsn-mimsy/openwsn-fw
sudo scons board=python toolchain=gcc oos_openwsn
cd /home/vagrant/openwsn-mimsy/openwsn-sw/software/openvisualizer 

(gnome-terminal -e "bash -c \"sudo scons runweb --sim --root='emulated1'; exec bash\"")
term1=$!
roscd beginner_tutorials
(gnome-terminal -e "bash -c \"rosrun beginner_tutorials node_handler.py; exec bash\"")
term2=$!
(gnome-terminal -e "bash -c \"rosrun beginner_tutorials openwsn_server.py; exec bash\"")
term3=$!
(gnome-terminal -e "bash -c \"rosrun beginner_tutorials openwsn_client.py 1 bbbb::1415:92cc:0:2; exec bash\"")
term4=$!




