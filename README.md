# RinGIF <img src="sample.gif" align="right" height=108/>

## Overview
<br>
RinGIF is a docker image that will automatically download Ring videos and convert them into GIFs<br>
These are useful for archiving, sharing, and for embedding in Home Assistant!<br>
<br>
## Requirements
- Ring doorbell or camera<br>
## Installation
<br>
# docker run -d --env email=myemailaddress@domain.com --env password=Password4MyRingAccount devinslick/ring_video_doorbell_gif

<br>
## Planned Features
- a web server inside the container for easier access<br>
- a variable to control the resolution of the gif<br>
- a variable to control the name of the video to save<br>
- a variable to control the name of the output gif<br>
<br>
## FAQ

* Where is my video/gif?*

- The latest video and gif will be kept on the docker volume mounted at /data.<br>
How am I supposed to get to the video/gif and share it?<br>
- You may want to consider sharing this volume with a web server.  You can also access it directly on your docker host.<br>
Why did you just add a webserver to this container?<br>
- See planned features above<br>
<br>
## Contributing
Please feel free to submit a pull request if you'd like to contribute to this code base!<br>
## Credits
This container would not be possible without the following awesome tools:<br>
https://github.com/tchellomello/python-ring-doorbell/<br>
-Marcelo Moreira de Mello (tchellmello)'s python SDK.<br>
-This tool allows us to query Ring's site and download videos as they become available.<br>
https://github.com/FFmpeg/FFmpeg<br>
-This is the tool RinGIF uses to extract images from the video.<br>
https://github.com/ImageMagick/ImageMagick<br>
-RinGIF uses this to create GIF from the extracted images.<br>
