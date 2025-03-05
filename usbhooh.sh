#!/bin/bash

# script to move over all files from a USB key
# when it is inserted into the system.

# should be called from a udev rule like:
#ACTION=="add",KERNEL=="sd*", SUBSYSTEMS=="usb", ATTRS{product}=="Mass Storage", RUN+="/root/bin/usbhook %k"

# Copyright 2009 Jason Antman.  
# 

# CONFIGURATION
DEBUG=1 # set to 1 for debugging output
DEST="/home/coope/coope-birthday/" # destination for files


DEVICE="$1" # the device name
LOGFACILITY="kernel.info" # for debugging output


if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook called with arguments: "$DEVICE"; fi

sleep 5 # delay 5 seconds to wait for mount
touch $DEST/foobarbaz.txt
echo "foobarbaz" > $DEST/foobarbaz.txt
fi

# mount | grep "$DEVICE"
# FOO="$?"

# if [ $FOO == 0 ];
# then
#     if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook device mounted: "$DEVICE"; fi
# else
#     if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook device NOT mounted: "$DEVICE" - exiting; fi
#     exit 0
# fi

# BAR=`mount | grep "$DEVICE" | awk '{ print $3 }'`

# if [ -e "$BAR/foobarbaz.txt" ]
# then
#     if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook "$BAR"/foobarbaz.txt found; fi
# else
#     if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook "$BAR"/foobarbaz.txt NOT found - exiting; fi
#     exit 0
# fi

# cp -R "$DEVICE"/* "$DEST"