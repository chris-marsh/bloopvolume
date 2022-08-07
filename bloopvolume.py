#!/usr/bin/env python

# BloobVolume - Volume control with audible and visible notification

import sys
import argparse
from subprocess import call
from pulsectl import Pulse


NOTIFICATION_ID = '6788'
DEFAULT_SOUND_FILE = '/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga'
DEFAULT_STEP = 5


def call_subprocess(command):
  """
  Run an external program
  Args:
    command (list): list of arguments
  Returns:
    boolean for success or failure
  """

  try:
    result = call(command) == 0
  except FileNotFoundError:
    return False
  else:
    return result


def playsound(sink_index, soundfile):
  """
  Use external program 'pactl' to play a sound file
  Args:
    sink_index (int): sink to use for output
    soundfile (str): full path of file to play
  Returns:
    boolean for success or failure
  """

  # pactl first needs the sound file stored on the server
  command = [
    "pactl", "upload-sample", soundfile, "volume-change"
  ]
  if call_subprocess(command):
    # if the upload succeeds we can play the sound
    command =[
      "pactl", "play-sample", "volume-change", str(sink_index)
    ]
    return call_subprocess(command)
  else:
    return False


def get_active_sink(pulse):
  """
  Use pulsectl to select the active sound sink
  A sink list is retrieved and iterated, the last found as 'running' is used
  If no sink is 'running', we default to the first entry
  Args:
    pulse (Pulse): an instance of pulsectl.Pulse
  Returns:
    PulseSinkInfo: an instance of pulsectl.PuleSinkInfo
  """

  active_sink = None
  sink_list = pulse.sink_list()
  for sink in sink_list:
    if sink.state == 'running':
      active_sink = sink
  if active_sink == None:
    active_sink = sink_list[0]
  return active_sink


def send_notification(volume, mute):
  """
  Use external program 'dunstify' to display a notification
  Args:
    volume (int): the volume level to display
    mute (bool): mute status
  Returns:
    boolean for success or failure
  """

  command = [
    "dunstify",
    "-r", NOTIFICATION_ID,
    "-u", "normal"
  ]

  if mute:
    mute_symbol='🔇'        # U+1F507
    command += [
      mute_symbol+" Volume: Mute",       # label to show mute
      "-h", "int:value:0"  # show zero bar to keep notification size
    ]

  else:
    if volume < 0.3:
      volume_symbol = '🔈'  # U+1F508
    elif volume < 0.6:
      volume_symbol = '🔉'  # U+1F509
    else:
      volume_symbol = '🔊' # U+1F50A
    command += [
      volume_symbol+" Volume: ",           # label as volume
      "-h",                 # pass hint and value to show progress bar
      "int:value:{:.0f}".format(volume*100)
    ]

  return call_subprocess(command)


def do_action(action, step=DEFAULT_STEP, sound_file=DEFAULT_SOUND_FILE):
  """
  Change volume of the active sound sink
  Args:
    action (str): options 'up', 'down' or 'mute'
    step (int): the amount to change the volume (up or down)
    sound_file (str): sound to play when notification is shown
  Returns:
    boolean for success or failure
  """

  with Pulse('volume-changer') as pulse:
    active_sink = get_active_sink(pulse)

    # round volume to nearest step value
    volume = step * round((active_sink.volume.value_flat * 100) / step)
    is_mute = (action == 'mute')

    if action == 'up':
      volume += step
      if volume > 150: volume = 150

    elif action == 'down':
      volume -= step
      if volume < 0: volume = 0

    elif action == 'mute':
      is_mute = not (active_sink.mute == 1)

    else:
      return False

    pulse.mute(active_sink, is_mute)
    pulse.volume_set_all_chans(active_sink, volume / 100)
    playsound(active_sink.index, sound_file)

    return send_notification(active_sink.volume.value_flat, is_mute)


def main():
  """
  entry point to parse command line arguments
  """
  parser = argparse.ArgumentParser(description='Pulseaudio volume controller')
  parser.add_argument('action', choices=['up', 'down', 'mute'])
  parser.add_argument('--step', dest='step', type=int, default=DEFAULT_STEP, help='Percentage to change the volume')
  parser.add_argument('--sound', dest='sound', default=DEFAULT_SOUND_FILE, help='Specify a sound file to play')

  args = parser.parse_args()
  do_action(args.action, args.step, args.sound)

if __name__ == "__main__":
  main()

