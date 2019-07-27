#!/bin/bash

# Script to launch audio servers for music-making.

case $1 in

  start )
    echo Starting JACK...

    # Start JACK
    # As of Ubuntu 12.10, a period of 128 is needed for good fluidsynth
    # timing.  (jackd 1.9.9, fluidsynth 1.1.5)
    # If you aren't running pulseaudio, you can remove the pasuspender line.
    pasuspender -- \
        jackd -d alsa --device hw:0 --rate 44100 --period 128 \
            &>/tmp/jackd.out &

    sleep .5

    #echo Starting fluidsynth...

    # Start fluidsynth
    fluidsynth --server --no-shell --audio-driver=jack \
        --connect-jack-outputs --reverb=0 --chorus=0 --gain=0.8 \
        /usr/share/sounds/sf2/FluidR3_GM.sf2 \
        &>/tmp/fluidsynth.out &

    sleep 1

    if pgrep -l jackd && pgrep -l fluidsynth
    then
      echo Audio servers running.
    else
      echo There was a problem starting the audio servers.
    fi

    # Use aconnect to get the ports
	keystationport=$(aconnect -i | grep "client.*Keystation" | cut -d ' ' -f 2)0
	synthport=$(aconnect -o | grep "FLUID Synth" | cut -d ' ' -f 2)0

	echo Keystation output port: $keystationport
	echo fluidsynth input port: $synthport

	# Connect the ports
	aconnect $keystationport $synthport

	while [ $? -ne 0 ]; do
		keystationport=$(aconnect -i | grep "client.*Keystation" | cut -d ' ' -f 2)0
		synthport=$(aconnect -o | grep "FLUID Synth" | cut -d ' ' -f 2)0

		echo Keystation output port: $keystationport
		echo fluidsynth input port: $synthport
		aconnect $keystationport $synthport
	done
		

    ;;

  stop )
    killall fluidsynth
    killall jackd
    echo Audio servers stopped.
    ;;

  * )
    echo Please specify start or stop...
    ;;
esac


