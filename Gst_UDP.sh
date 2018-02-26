#!/bin/bash
gst-launch-1.0 -v v4l2src device="/dev/video0" ! video/x-raw,width=1280,height=720 ! queue !  jpegenc ! rtpjpegpay ! udpsink host="127.0.0.1" port="7331"
