# BloopVolume

A command line volume control with visual and audible desktop notification.

![BloopVolume Notification](/screenshots/screen1.jpg?raw=true "BloopVolume Notification")
![BloopVolume Mute Notification](/screenshots/screen2.jpg?raw=true "BloopVolume Mute Notification")

## Why?

There are many volume control scripts out there, but my motivation for writing bloopvolume were:

1. Portable across any linux desktop environment or window manager
2. Able to control the current audio output either speaker or headphone
3. Play notification sound through the current active audio source

## Requirements

* [Python](https://www.python.org/)
* [PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/)
* [Dunst](https://dunst-project.org/)

## Installation
### Installing from github
```
$ git clone https://github.com/chris-marsh/bloopvolume.git
$ cd bloopvolume
$ pip install -r requirements.txt
```
If you don't have the 'pip' command:
```
$ python -m ensurepip
$ python -m pip install --upgrade pip
$ python -m pip -r requirements.txt
```

## Command line usage
```
bloopvolume.py [OPTION] up | down | mute
  --step    Amount to change the volume by
  --sound   qualified path to sound file to play for notification
```

bloopvolume will use default values for step and sound if not specified:
```
step default    5
sound default   /usr/share/sounds/freedesktop/stereo/audio-volume-change.oga
```
## Examples
```
$ bloopvolume.py up
$ bloopvolume.py --step 10 down  
$ bloopvolume.py --sound /home/user/beep.mp3 --step 4 up  

```
# Window Manager Example Configs

### Qtile
```
keys = [
    ...
    Key([], "XF86AudioRaiseVolume",lazy.spawn("/home/user/bloopvolume.py up")),
    Key([], "XF86AudioLowerVolume",lazy.spawn("/home/user/bloopvolume.py down")),
    Key([], "XF86AudioMute",lazy.spawn("/home/user/bloopvolume.py mute")),
    ....
]
```

## i3
```
bindsym XF86AudioRaiseVolume exec --no-startup-id /home/user/bloopvolume.py up
bindsym XF86AudioLowerVolume exec --no-startup-id /home/user/bloopvolume.py down
bindsym XF86AudioMute exec --no-startup-id /home/user/bloopvolume.py mute
```
## Links

* [python-pulse-control](https://github.com/mk-fg/python-pulse-control) used in this project to control PulseAudio

## Copyright

Copyright 2022 Chris Marsh and contributors (see [LICENSE](/LICENSE.md) for licensing information)
