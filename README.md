# RinGIF
Turn your ring doorbell videos into a GIFs to review them for suspicious activity.

Prerequisites:
-CentOS 7.   This is the only distribution I am actively testing on. 
-A Ring doorbell or camera with a subscription.  
-wget

Includes:
-Python 2.7/3x
-ring_doorbell pip package
-jpegtran (for jpeg optimization)
-ImageMagick tools (to create the GIF)

How to install:
bash -c "$(wget -qO - https://raw.githubusercontent.com/devinslick/RinGIF/master/extras/installer.sh)"

