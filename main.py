from ring_doorbell import Ring
import os
import csv
import time
import datetime
 
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
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": " + type + str(d) + ", recording " + str(device.last_recording_id) + " was already saved.")                                                               
  else:                                                                                                         
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Getting recording URL for " + type + " #" + i + ". RecordingID: " + str(device.last_recording_id) )
    url=str(device.recording_url(doorbells.last_recording_id))                                            
    if "https" not in url:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Invalid URL returned.  Exiting")
      sys.exit(1)
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ': Starting download for ' + type + ' #' + i + '. Recording: ' + str(device.last_recording_id) )                     
    wgetCmd = 'wget -O /data/' + type + i +'.mp4 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2460.41 Safari/537.36" "'+url+'"' 
    os.system(wgetCmd)                                                                                                                        
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Download complete, starting ffmpeg")
    (                                                                                                                                         
      ffmpeg                                                                                                                                  
      .input('/data/' + type + i + '.mp4')                                                                                                  
      .filter('fps', fps=fps, round='up')                                                                                                       
      .output('/data/' + type + i + '-%03d.jpg')                                                                                            
      .run()                                                                                                                                  
    )                                                                                                                                         
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": ffmpeg complete, starting jpeg optimization")
    jpgCmd = 'jpegoptim -f -q -s /data/' + type + i + '-*.jpg'                                  
    os.system(jpgCmd)                                                                                      
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": jpeg optimization complete, creating gif")
    gifCmd = 'convert -delay 20 -loop 0 /data/' + type + i + '*.jpg -resize ' + resolution + ' /data/' + type + i + '.gif'                 

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


#for chimes in myring.doorbells:
#for stickup_cams in myring.doorbells:

