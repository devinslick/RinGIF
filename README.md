# RinGIF

<img src="sample.gif" align="right" height=108/>

RinGIF is a docker image that will automatically download Ring videos and 
convert them into GIFs.
These are useful for archiving, sharing, and for embedding in Home Assistant!

## Requirements
- Ring Doorbell / Camera with a paid subscription


## Examples

```bash
docker run -d --env email=myemailaddress@domain.com --env password=MySecretPass --name RinGIF-Example-1 devinslick/ring_video_doorbell_gif

#Use non-default file names in the output
docker run -d --env email=myemailaddress@domain.com --env password=MySecretPass --env vidName=doorbell.mp4 --env gifName=doorbell.gif --name RinGIF-Example-2 devinslick/ring_video_doorbell_gif

#Get a higher quality image from your second Ring device
docker run -d --env email=myemailaddress@domain.com --env password=MySecretPass --env fps=2 --env resolution 284x216 --env doorbell=1 --name RinGIF-Example-3 devinslick/ring_video_doorbell_gif


```

## Environmental Variables

| ENV  | Default Value| Required | Note |
| ------------- | ------------- | ------------- | ------------- |
| email | emailaddress@notdefined.yet | True | Email associated with your Ring account, must be defined |
| password  | undefined  | True | Password for your Ring account, must be defined  |
| doorbell  | 0  | False | Index of the doorbell/camera on your account to use for this container |
| fps  | 1  | False | Change to increase the number of frames per second |
| resolution | 192x108 | False | Controls the GIF output resolution |
| vidName | last_recording.mp4 | False | Change to control the output video file name |
| gifName | latest.gif | False | Change to control the output GIF file name |

## Planned Features
- a web server inside the container for easier access
- continually loop to check Ring, stop using a minute cronjob 

## FAQ
- Where is my video/gif?

  The latest video and gif will be kept on the docker volume mounted at /data.

- How am I supposed to get to the video/gif and share it?

  You may want to consider sharing this volume with a web server. 
  You can also access it directly on your docker host.
- Why did you just add a webserver to this container?

  See planned features above

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests and this README as appropriate.

## Credits
[Ring SDK](https://github.com/tchellomello/python-ring-doorbell/) is used to query Ring servers and download new videos when available.

[ffmpeg](https://github.com/FFmpeg/FFmpeg) is used to extract images from the videos.

[ImageMagick](https://github.com/ImageMagick/ImageMagick) is used to create GIFs from extracted images.
