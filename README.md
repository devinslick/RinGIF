# RinGIF

<img src="sample.gif" align="right" height=108/>

RinGIF is a docker image that will automatically download Ring videos and 
convert them into GIFs.  It will loop through all of your ring camera devices,
check for new videos, download them, create JPGs, and then turn these into GIFs.
These are great for quick review of security events, for archiving, sharing, and for embedding in Home Assistant!

## Requirements
- Ring Doorbell / Camera with a paid subscription


## Examples

```bash
#Minimal example with web server on port 8735
docker run -d -p=8735:8735/tcp --env email=myemailaddress@domain.com \
--env password=MySecretPass \
--name RinGIF-Example-1 \
devinslick/ring_video_doorbell_gif

#Get a higher quality images, add timezone, publish port to port assigned by Docker
docker run -d --publish-all --env email=myemailaddress@domain.com \
--env password=MySecretPass \
--env fps=2 \
--env resolution 284x216 \
--env timezone America/New_York
--name RinGIF-Example-2 \
devinslick/ring_video_doorbell_gif

```

## Environmental Variables

| ENV  | Default Value| Required | Note |
| ------------- | ------------- | ------------- | ------------- |
| email | emailaddress@notdefined.yet | True | Email associated with your Ring account, must be defined |
| password  | undefined  | True | Password for your Ring account, must be defined  |
| fps  | 1  | False | Change to increase the number of frames per second |
| resolution | 192x108 | False | Controls the GIF output resolution |
| timezone | America/Chicago | False | Only used for logs to stdout |

## Planned Features
- a web server inside the container for easier access

## FAQ
- Where is my video/gif?

  Only the latest videos and GIFs are kept in this container.  They can be found under /data in the container.
  I'm considering adding archiving functionality to this container.  Stay tuned!

- How am I supposed to get to the video/gif and share it?

  The embedded web server should make it easy to view, download, or share your content.
  Inside the container, this web server runs on port 8735.  If you used the syntax from example 1, it will be port 8735 on your docker host.
  If you're logged into your docker host an example URL would be http://localhost:8735/doorbell0.gif.
  If your docker machine is somewhere else on your network, use its IP address instead: http://192.168.1.43:8735/doorbell0.gif.

- What are valid timezones for the timezone ENV variable?

  You can find a complete list of options here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update this README with usage and examples.

## Credits
[Ring SDK](https://github.com/tchellomello/python-ring-doorbell/) is used to query Ring servers and download new videos when available.

[ffmpeg](https://github.com/FFmpeg/FFmpeg) is used to extract images from the videos.

[ImageMagick](https://github.com/ImageMagick/ImageMagick) is used to create GIFs from extracted images.
