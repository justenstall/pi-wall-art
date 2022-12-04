#!/usr/bin/env python

from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown():
    check_call(['sudo', 'shutdown', '-h', 'now'])

shutdown_btn = Button(3, hold_time=1)
shutdown_btn.when_held = shutdown

pause()

# Copy to /usr/local/bin
# sudo cp shutdown-button.py /usr/local/bin