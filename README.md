# RinGIF

<img src="sample.gif" align="right" height=108/>

RinGIF is a docker image that will automatically download Ring videos and 
convert them into GIFs.  It will loop through all of your ring camera devices,
check for new videos, download them, and create a GIF for you using the most interesting frames.
You'll usually see a 20MB video convert down to under 100KB.
These are great for quick review of security events, archiving, sharing, and for embedding in Home Assistant!

## Requirements
- Ring Doorbell, Chime, and/or Stick-up Cameras with a paid subscription


## Examples

```bash
#Minimal example with web server on port 8735
docker run -d -p=8735:8735/tcp --env email=myemailaddress@domain.com \
--env password=MySecretPass \
--name RinGIF-Example-1 \
devinslick/ring_video_doorbell_gif

#Add timezone, resolution, and publish port to port assigned by Docker
docker run -d --publish-all --env email=myemailaddress@domain.com \
--env password=MySecretPass \
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
| timezone | America/Chicago | False | Only used for logs to stdout |
| resolution | 192x108 | False | Controls the GIF output resolution |

## Planned Features
- gif/mp4 archiving, retention schedules

## FAQ
- Where is my video/gif?

  Only the latest videos and GIFs are kept in this container.  They can be found under /data or accessed via the built in web server.

- How am I supposed to get to the video/gif and share it?

  The embedded web server should make it easy to view, download, or share your content.
  Inside the container, this web server runs on port 8735.  If you used the syntax from example 1, it will be port 8735 on your docker host.  If you're running docker locally, you can navigate to the web server by going to http://localhost:8735/.  
  Here you'll find videos and gifs for each of your Ring stickup cams, doorbells, and chimes.

- What are valid timezones for the timezone ENV variable?

  You can find a complete list of options here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

- What if one of my Ring devices doesn't have a subscription?

  RinGIF won't be able to download videos for that device.

- What if I only want RinGIF to run against a subset of the Ring devices on my account?

  Create a new Ring account for RinGIF and share the cameras with this account.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update this README with usage and examples.

## Credits
[Ring SDK](https://github.com/tchellomello/python-ring-doorbell/) is used to query Ring servers and download new videos when available.

[ffmpeg](https://github.com/FFmpeg/FFmpeg) is used to extract images from the videos.

[ImageMagick](https://github.com/ImageMagick/ImageMagick) is used to create GIFs from extracted images.
