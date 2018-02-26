#!/bin/bash
gst-launch-1.0 -v\
        v4l2src device="/dev/video0" \
        ! tee name=alpha !queue !  videoconvert ! videoscale ! video/x-raw,width=320,height=240 \
        ! clockoverlay shaded-background=true font-desc="Sans 38" \
        ! theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=7331 alpha. ! queue !  clockoverlay shaded-background=true font-desc="Sans 38" ! autovideosink
