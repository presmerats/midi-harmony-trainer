aconnect -l 
  245  pgrep -l jackd 
  246  jackd -d alsa --device hw:0 --rate 44100 --period 128             &>/tmp/jackd.out &
  247  jackd -d alsa --device hw:0 --rate 44100 --period 128 \
  248  fluidsynth --server --no-shell --audio-driver=jack         --connect-jack-outputs --reverb=0 --chorus=0 --gain=0.8         /usr/share/sounds/sf2/FluidR3_GM.sf2         &>/tmp/fluidsynth.out &
  249  pgrep -l jackd
  250  pgrep -l fluidsynth
  251  aconnect -i
  252  aconnect -o
  253  aconnect 20 128
  254  python3 miditrainer.py 
  255  pip3 install mido==1.2.9 python-rtmidi==1.3.0 py-picotts pprint==0.1
  256  pip3 install mido==1.2.9 python-rtmidi==1.3.0 py-picotts pprint
  257  python3 miditrainer.py 
  258  python3
  259  python
  260  pip3 install mido==1.2.9
  261  python3
  262  python3 miditrainer.py 
  263  pip3 install mingus==0.6.1


$ sudo apt-get install git
$ sudo git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
$ sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
$ sudo apt-get install python3-dev
$ cd pyaudio
$ sudo python3 setup.py install

sudo nano /usr/local/lib/python3.5/dist-packages/PyAudio-0.2.14-py3.5-linux-i686.egg/pyaudio/__init__.py
	modify   removing f" to "

modify code for _silent.py version

pip3 install python-rtmidi==1.0.3

