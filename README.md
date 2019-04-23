# RinGIF
Turn your ring doorbell videos into a GIFs to review them for suspicious activity.

Prerequisites:
-A Ring doorbell or camera with a subscription.  

Define the environmental variables listed in the docker file to configure:

email: this is the email address associated with your Ring doorbell account
password: your Ring password
doorbell: this defaults to 0, using your 1st doorbell. Change this to switch between cameras if you have multiple.
fps: this is how many frames per second to use for the gif, defaults to 1
archivePath: not in use yet, intended to provide a way to store images

More usage information to come, eventually...


Planned features
-a web server inside the container for easier access
-a variable to control the resolution of the gif
-a variable to control the name of the video to save
-a variable to control the name of the output gif
