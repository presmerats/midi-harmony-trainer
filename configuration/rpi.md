------base-----
ok- intervals
ok- chords
ok- Key signatures
- button function switch (3 button-3 led interface + audio)
	- movement: random, 4rths, semitone
	- type: Maj7, 7, min7, half-dim, dim, sus4, ext-Maj7, ext-7, ext-min7, ext-half-dim
	- program:  intervals, chords, scales, progressions, patterns
- score answer
- piano answer
- guitar answer
------comp---------
- II-V-I progressions
- chords inversions
- chords drop 2
- chords drop 2 inversions
- chords drop 3
- chords drop 3 inversions
- piano comp chords: confort
- piano comp chords: ...
- guitar comp chords: confort pos
- guitar comp chords: drop2
-----soloing----------
- Scales:
	ok- major, natural minor, harmonic minor, melodic minor
	- major pentatonic, minor pentatonic
	- ionian, doric, phrigian, lidian, mixolydian, aeloian, locrian
	- whole tone, diminished scale(half-whole tone), whole-half tone
- guitar chord-melody: 
-----system--------------

- wifi dongle
	https://www.lifewire.com/usb-wifi-adapter-raspberry-pi-4058093
- ssh setup
    
- python and repo setup
```
git clone https://github.com/presmerats/midi-harmony-trainer.git
```
- audio setup from scratch
    + sudo apt install git python-dev python-pip python3 alsa-utils vim fluidsynth python3-pip python3-dev fluid-soundfont-gm jackd2 jack-tools pulseaudio python-pyaudio
    + Enable realtime priority set to no
    + #set raspi-config pi user autologin  
    + add .bashrc lines to midi user
```
/home/pi/midi-harmony-trainer/mido/config.sh start
/usr/bin/amixer set Master 100%
/usr/bin/aplay -D hw:0 /usr/share/sounds/alsa/Side_Right.wav

```
- picotts setup
```
wget -q https://ftp-master.debian.org/keys/release-10.asc -O- | sudo apt-key add -
echo "deb http://deb.debian.org/debian buster non-free" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install libttspico-utils
```
- python2 setup
    + pip install mido mingus py-picotts
- python3 port 
    + rewrite mingus adapted to python3 syntax, only mingus.core.chords
    + pyaudio
```
$ sudo apt-get install git
$ sudo git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
$ sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
$ sudo apt-get install python3-dev
$ cd pyaudio
$ sudo python3 setup.py install
```

- python3 pyaudio? 
- GPIO setup
    +  GPIO tests button + leds
    +  add button logic: idle, chords, intervals, scales