cd /scripts/ring
username=$(<variables/username)
password=$(<variables/password)
mv variables/recording variables/recording.last
python python/check_last_recording.py $username $password
head -c 75 variables/recording.current > variables/recording
rm -rf variables/recording.current
df=$(diff variables/recording.last variables/recording | wc -l)
if [ "$df" -ne "0" ];then
  timestamp=$(date +%Y%m%d%H%M%S)
  echo "Downloading a new doorbell video... $timestamp"
  python python/download_last_recording.py $username $password;

  #archive to NAS
  #mkdir -p /media/ring/videos
  #cp www/videos/last_recording.mp4 /media/ring/videos/$timestamp.mp4

  #create JPG images from video
  ffmpeg -i www/videos/last_recording.mp4 -vf fps=1 "www/frames/frame-%03d.jpg" -hide_banner
 
  #optimize images
  find $(pwd)/www/frames -name "*.jpg" -type f -exec jpegtran -copy none -optimize -outfile {} {} \;
  
  #downsize and convert to a GIF
  /usr/local/bin/gm convert -size 192x108 -despeckle -dither -delay 20 -loop 0 $(pwd)/www/frames/*.jpg -resize 192x108 www/images/latest.gif
  
  #clear the JPG folder
  rm -rf www/frames/*

  #archive a copy of the GIF
  /usr/bin/cp www/images/latest.gif /media/ring/$(date +%Y%m%d%H%M%S).gif

  echo "New doorbell video processed"
  echo "$(date)"
fi
