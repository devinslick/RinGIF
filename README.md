# RinGIF

<img src="sample.gif" align="right" height=108/>

RinGIF is a docker image that will automatically download Ring videos and 
convert them into GIFs.
These are useful for archiving, sharing, and for embedding in Home Assistant!

## Requirements
- Ring Doorbell / Camera with a paid subscription


## Examples

```bash
#Minimal example
docker run -d --env email=myemailaddress@domain.com \
--env password=MySecretPass \
--name RinGIF-Example-1 \
devinslick/ring_video_doorbell_gif
/

#Get a higher quality images
docker run -d --env email=myemailaddress@domain.com \
--env password=MySecretPass \
--env fps=2 \
--env resolution 284x216 \
--name RinGIF-Example-2 \
devinslick/ring_video_doorbell_gif
/

```

## Environmental Variables

| ENV  | Default Value| Required | Note |
| ------------- | ------------- | ------------- | ------------- |
| email | emailaddress@notdefined.yet | True | Email associated with your Ring account, must be defined |
| password  | undefined  | True | Password for your Ring account, must be defined  |
| fps  | 1  | False | Change to increase the number of frames per second |
| resolution | 192x108 | False | Controls the GIF output resolution |

## Planned Features
- a web server inside the container for easier access

## FAQ
- Where is my video/gif?

  The latest videos and gifs will be kept on the docker volume mounted at /data.

- How am I supposed to get to the video/gif and share it?

  You may want to consider sharing this volume with a web server. 
  You can also access it directly on your docker host.
- Why did you just add a webserver to this container?

  See planned features above

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update this README with usage and examples.

## Credits
[Ring SDK](https://github.com/tchellomello/python-ring-doorbell/) is used to query Ring servers and download new videos when available.

[ffmpeg](https://github.com/FFmpeg/FFmpeg) is used to extract images from the videos.

[ImageMagick](https://github.com/ImageMagick/ImageMagick) is used to create GIFs from extracted images.
