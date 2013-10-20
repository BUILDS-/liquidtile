#!/usr/bin/bash

# Setup Alsa Mixer so the default channel captures from the PCM Mix
amixer set 'Mix' cap
amixer set 'Capture' cap
amixer set 'Capture' 100%

