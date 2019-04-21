mkdir -p /data
touch /data/previous.recording
results=$(python /check_last_recording.py)
if [[ $results = *Updates* ]]
then
   echo "Download complete, beginning image extraction..."
   /usr/bin/ffmpeg -i "/data/last_recording.mp4" -vf fps=$fps "/data/frame-%03d.jpg" -hide_banner
   #optimize images
   find /data/ -name "*.jpg" -type f -exec jpegtran -copy none -optimize -outfile {} {} \;
   #downsize and convert to a GIF
   echo "Building GIF..."
   /usr/bin/convert -size 192x108 -despeckle -dither -delay 20 -loop 0 /data/*.jpg -resize 192x108 /data/latest.gif
   #delete the JPGs
   rm -rf /data/*jpg
   # optional feature to be added using the archivePath environmental variable
   # /usr/bin/cp /data/images/latest.gif $archivePath/$(date +%Y%m%d%H%M%S).gif
fi
