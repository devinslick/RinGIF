# RinGIF

<img src="sample.gif" align="right" height=108/>

RinGIF is a docker image that will automatically download Ring videos and convert them into GIFs
These are useful for archiving, sharing, and for embedding in Home Assistant!

## Requirements
-Ring Doorbell or Camera with subscription


## Installation


```bash
docker run -d --env email=myemailaddress@domain
```

## Environmental Variables

| ENV  | Default Value| Required | Note |
| ------------- | ------------- | ------------- | ------------- |
| email | emailaddress@notdefined.yet | True | Email associated with your Ring account, must be defined |
| password  | undefined  | True | Password for your Ring account, must be defined  |
| doorbell  | 0  | False | Index of the doorbell/camera on your account to use for this container |
| fps  | 1  | False | Frames per second to save in the GIF |

## Planned Features
- a web server inside the container for easier access
- a variable to control the resolution of the gif
- a variable to control the name of the video to save
- a variable to control the name of the output gif

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
