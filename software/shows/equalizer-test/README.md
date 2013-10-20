Experimenting with getting loop back audio and using pyaudio and numpy to analyze it!


http://alsa.opensrc.org/Record_from_pcm

## OSX Setup (Recording audio output from your sound card)

- Download and install [pyaudio](http://people.csail.mit.edu/hubert/pyaudio/) (and other required libraries). 

- Then go and get [Soundflower](http://cycling74.com/products/soundflower/) for free from Cycling74, install and reboot.

- Open up Soundflowerbed.

- Click on the little flower now on your menubar
  - Under Soundflower (2 ch) click Built-In Audio.

- Go to system preferences and then sound.

- Go to the Output tab and select Soundflower (2ch) as your audio interface by clicking on it.
  you can alter the volume here if you want.

- If you are playing music and you go to Input, when you click on 
  Soundflower (2ch) you should be able to see the little VU meter bar
  bouncing to the music.

- Figure out what interface number you are dealing with. In general you will be sampling at 48kHz and
  on my Mac my input device index was 2, this may be different on your system. Experiment until
  you get the audio working.
