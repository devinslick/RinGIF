from ring_doorbell import Ring
import os
import csv
import time
import datetime
import wget
 
email = str(os.environ['email'])
password = str(os.environ['password'])
resolution = str(os.environ['resolution'])

def log(device,message):
  timestamp=datetime.datetime.now().replace(microsecond=0).isoformat()
  line = timestamp + ", " + device + ", " + message
  print(line)

def isLatest(recordingID):                                                              
  if os.path.exists('/data/device_tracking.db'):
    with open('/data/device_tracking.db', 'rt') as f:                                           
      reader = csv.reader(f, delimiter=',')                                               
      for row in reader:                                                                  
        if str(recordingID) == row[2]:                                                    
          return "true"                                                                   
      return "false" 
  else:
    with open('/data/device_tracking.db', 'w+') as db:
      db.write('DeviceType,DeviceID,RecordingID\n')
    return "false"

def mp4optimizer(file,sensitivity="0.015"):
  #remove duplicate frames.  .03 is good, too aggressive?
  ffmpegCmd1 = 'ffmpeg -i /data/' + file + '.mp4 -an -vf "select=gt(scene\,' + sensitivity + '),setpts=N/(10*TB)" /data/' + file + '-sense.mp4'
  os.system(ffmpegCmd1)
  #trim the duplicate frames
  ffmpegCmd2 = 'ffmpeg -i /data/' + file + '-sense.mp4 -an -vf "mpdecimate" /data/' + file + '-trim.mp4 > /dev/null 2>&1'
  os.system(ffmpegCmd2)

def extractframes(file):
  extractCmd = 'ffmpeg -i /data/' + file + '-trim.mp4 -r 1/1 /data/' + file + '%03d.jpg'
  os.system(extractCmd)

def deviceCheck(device,type,i):
  if isLatest(device.last_recording_id) == 'true':
    log(type + str(i), "recording " + str(device.last_recording_id) + " was already saved.")
  else:
    log(type + str(i), "getting URL for recording " + str(device.last_recording_id))
    url=str(device.recording_url(device.last_recording_id))       
    if "https" not in url:
      log(type + str(i), "invalid URL! Exiting")
      sys.exit(1)
    log(type + str(i), "starting download for recording " + str(device.last_recording_id))
    wgetCmd = 'wget -O /data/' + type + str(i) + '.mp4 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2460.41 Safari/537.36" "' + url + '"'
    os.system(wgetCmd)
    log(type + str(i), "video downloaded, beginning optimization")
    mp4optimizer(type + str(i))
    log(type + str(i), "mp4 optimized, extracting jpegs")
    extractframes(type + str(i))
    log(type + str(i), "jpeg extraction complete, starting jpeg optimization")
    jpgCmd = 'jpegoptim -f -q -s /data/' + type + str(i) + '*.jpg'                                  
    os.system(jpgCmd)                                                                                      
    log(type + str(i), "jpeg optimization complete, creating GIF")
    gifCmd = "convert -delay 20 -loop 0 /data/" + type + str(i) + "*.jpg -resize " + resolution + " /data/" + type + str(i) + ".gif"
    os.system(gifCmd)                                                                                      
    with open('/data/device_tracking.db', mode='a') as db:                
      dbo = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                                                          
      dbo.writerow([type, i, str(device.last_recording_id)])   
    os.system('rm -f /data/*.jpg')
    os.system('rm -f /data/*-trim.mp4')
    os.system('rm -f /data/*-sense.mp4')

os.system("rm -f /data/*.jpg")  
while True:
  try:
    if myring.is_connected != True:
      log("Ring.com", "connection time out, reconnecting...")
      myring = Ring(email, password)
    if myring.is_connected == True:
      log("Ring.com", "connection healthy")
      for d, doorbell in enumerate(myring.doorbells):
        deviceCheck(doorbell,"doorbell",d)
      for s, stickup in enumerate(myring.stickup_cams):
        deviceCheck(stickup,"stickup",s)
      for c, chime in enumerate(myring.chimes):
        deviceCheck(chime,"chime",c)
      time.sleep(5)
  except NameError:
    log("Ring.com", "connecting")
    myring = Ring(email, password)

