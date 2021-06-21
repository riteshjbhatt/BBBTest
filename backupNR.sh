#!/bin/bash
today=$(date +"_%y%m%d_%H%M%S")
echo $today
echo
filename="/home/debian/nodeRedBackups/flows_beaglebone$today.json"
echo $filename
echo
cp -f /var/lib/node-red/.node-red/flows_beaglebone.json $filename
