#!/bin/bash
gst-launch-1.0 -v v4l2src device="/dev/video0" ! autovideosink
