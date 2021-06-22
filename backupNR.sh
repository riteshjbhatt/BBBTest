#!/bin/bash
today=$(date +"_%y%m%d_%H%M%S")
filename="/home/debian/nodeRedBackups/flows_beaglebone$today.json"
cp -f /var/lib/node-red/.node-red/flows_beaglebone.json $filename
