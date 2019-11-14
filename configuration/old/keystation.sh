#!/bin/bash

# Launch vmpk and connect it to fluidsynth.
# Based on a script by Antonio Bonifati.

# If vmpk isn't running
#if ! pgrep "^vmpk$"
#then
#    # Launch vmpk
#    vmpk &
#    # Wait for it to come up.
#    sleep 1
#fi

# Use aconnect to get the ports
keystationport=$(aconnect -i | grep "client.*Keystation" | cut -d ' ' -f 2)0
synthport=$(aconnect -o | grep "FLUID Synth" | cut -d ' ' -f 2)0

echo Keystation output port: $keystationport
echo fluidsynth input port: $synthport

# Connect the ports
aconnect $keystationport $synthport

	