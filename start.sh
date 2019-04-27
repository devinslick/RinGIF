pythonRunning=$(ps -ef | grep python | wc -l)
if [[ $pythonRunning == "1" ]]; then
  touch /data/previous.recording
  results=$(python /download.py)
  if [[ $results == "Updates" ]]; then
    echo "Download complete, beginning image extraction..."
    /usr/bin/ffmpeg -i "/data/$vidName" -vf fps=$fps "/data/frame-%03d.jpg" -hide_banner
    #optimize images
    find /data/ -name "*.jpg" -type f -exec jpegtran -copy none -optimize -outfile {} {} \;
    #downsize and convert to a GIF
    echo "Building GIF..."
    /usr/bin/convert -delay 20 -loop 0 /data/*.jpg -resize $resolution /data/$gifName
    #delete the JPGs
    rm -rf /data/*jpg
    # optional feature to be added using the archivePath environmental variable
    # /usr/bin/cp /data/images/latest.gif $archivePath/$(date +%Y%m%d%H%M%S).gif
  fi
fi
