from ring_doorbell import Ring
import os
import csv
import time
import datetime
import ffmpeg
import wget
 
email = str(os.environ['email'])
password = str(os.environ['password'])
resolution = str(os.environ['resolution'])
fps = str(os.environ['fps'])

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

def deviceCheck(device,type,i):
  if isLatest(device.last_recording_id) == 'true':
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": " + type + str(i) + ", recording " + str(device.last_recording_id) + " was already saved.")
  else:
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Getting recording URL for " + type + " #" + str(i) + ". RecordingID: " + str(device.last_recording_id) )
    url=str(device.recording_url(device.last_recording_id))       
    if "https" not in url:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Invalid URL returned.  Exiting")
      sys.exit(1)
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ': Starting download for ' + type + ' #' + str(i) + '. Recording: ' + str(device.last_recording_id) ) 
    wgetCmd = 'wget -O /data/' + type + str(i) +'.mp4 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2460.41 Safari/537.36" "' + url + '"'
    os.system(wgetCmd)
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Download complete, starting ffmpeg")
    (                                                                                                                                         
      ffmpeg                                                                                                                                  
      .input('/data/' + type + str(i) + '.mp4')                                                                                                  
      .filter('fps', fps=fps, round='up')                                                                                                       
      .output("/data/" + type + str(i) + "%03d.jpg")                                                                                            
      .run()                                                                                                                                  
    )                                                                                                 
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": ffmpeg complete, starting jpeg optimization")
    jpgCmd = 'jpegoptim -f -q -s /data/' + type + str(i) + '*.jpg'                                  
    os.system(jpgCmd)                                                                                      
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": jpeg optimization complete, creating gif")
    gifCmd = "convert -delay 20 -loop 0 /data/" + type + str(i) + "*.jpg -resize " + resolution + " /data/" + type + str(i) + ".gif"
    os.system(gifCmd)                                                                                      
    with open('/data/device_tracking.db', mode='a') as db:                
      dbo = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                                                          
      dbo.writerow([type, i, str(device.last_recording_id)])   
    os.system('rm -f /data/*.jpg')


os.system("rm -f /data/*.jpg")  
while True:
  try:
    if myring.is_connected != True:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Existing Ring.com connection has timed out, reconnecting...")
      myring = Ring(email, password)
    if myring.is_connected == True:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Ring.com connection is healthy.")
      for d, doorbell in enumerate(myring.doorbells):
        deviceCheck(doorbell,"doorbell",d)
      for s, stickup in enumerate(myring.stickup_cams):
        deviceCheck(stickup,"stickup",s)
      for c, chime in enumerate(myring.chimes):
        deviceCheck(chime,"chime",c)
      time.sleep(5)
  except NameError:
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Connecting to Ring.com.")
    myring = Ring(email, password)

