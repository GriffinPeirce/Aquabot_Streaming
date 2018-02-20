#/bin/bash/
gst-launch-1.0 -v udpsrc port=7330 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink &
gst-launch-1.0 -v udpsrc port=7331 ! application/x-rtp, encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink
