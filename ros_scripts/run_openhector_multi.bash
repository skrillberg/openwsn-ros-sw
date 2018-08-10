#!/bin/bash

sudo pkill -9 python 
pid=$!
wait $pid

gnome-terminal --window-with-profile=hold_profile -e "roslaunch hector_quadrotor_gazebo empty_world.launch"
sleep 10
counter=1
while [ $counter -le 3 ]
do
gnome-terminal --window-with-profile=hold_profile -e "roslaunch hector_quadrotor_gazebo x_quadrotors_empty_world.launch nr:=$counter"
rosservice call gazebo/pause_physics
sleep 20
rosservice call uav$counter/enable_motors "enable: true"
((counter++))
done

cd /home/muminovic/Desktop/openwsn-ros/openwsn-fw
sudo scons board=python toolchain=gcc oos_openwsn

roscd beginner_tutorials
(gnome-terminal -e "bash -c \"rosrun openwsn_ros node_handler.py; exec bash\"")

sleep 1
cd /home/muminovic/Desktop/openwsn-ros/openwsn-sw/software/openvisualizer 

(gnome-terminal -e "bash -c \"sudo scons runweb --sim --simCount=3 --root='emulated1'; exec bash\"")
term1=$!

roscd &

(gnome-terminal -e "bash -c \"rosrun openwsn_ros openwsn_server.py; exec bash\"")

term3=$!
(gnome-terminal -e "bash -c \"rosrun openwsn_ros openwsn_client.py 1 bbbb::1415:92cc:0:2; exec bash\"")
term4=$!





rqt_console



