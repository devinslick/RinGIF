from ring_doorbell import Ring
import os
import csv
import time
import ffmpeg
import wget
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

os.system("rm -f /data/*.jpg")  

while True:
  try:
    if myring.is_connected != True:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Existing Ring.com connection has timed out, reconnecting...")
      myring = Ring(email, password)
    if myring.is_connected == True:
      print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Ring.com connection is healthy.")
      d=0                                                                 
      for doorbells in myring.doorbells:                                  
        if isLatest(doorbells.last_recording_id) == 'true':               
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Doorbell " + str(d) + ", recording " + str(doorbells.last_recording_id) + " was already saved.")                                                               
        else:                                                                                                         
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Getting recording URL for doorbell #" + str(d) + ". RecordingID: " + str(doorbells.last_recording_id) )
          url=str(doorbells.recording_url(doorbells.last_recording_id))                                            
          if "https" not in url:
            print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Invalid URL returned.  Exiting")
            sys.exit(1)
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ': Starting download for doorbell #' + str(d) + '. Recording: ' + str(doorbells.last_recording_id) )                                 
          wgetCmd = 'wget -O /data/doorbell'+str(d)+'.mp4 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2460.41 Safari/537.36" "'+url+'"' 
          os.system(wgetCmd)                                                                                                                        
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Download complete, starting ffmpeg")                                                                                               
          (                                                                                                                                         
            ffmpeg                                                                                                                                  
            .input("/data/doorbell"+str(d)+".mp4")                                                                                                  
            .filter('fps', fps=fps, round='up')                                                                                                       
            .output("/data/doorbell"+str(d)+"-%03d.jpg")                                                                                            
            .run()                                                                                                                                  
          )                                                                                                                                         
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": ffmpeg complete, starting jpeg optimization")                                                                                      
          jpgCmd = "jpegoptim -f -q -s /data/doorbell"+str(d)+"*.jpg"                                                                               
          os.system(jpgCmd)                                                                                                                         
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": jpeg optimization complete, creating gif")                                                                                         
          gifCmd = "convert -delay 20 -loop 0 /data/doorbell"+str(d)+"*.jpg -resize " + resolution + " /data/doorbell" + str(d) + ".gif"                 
          os.system(gifCmd)                                                               
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": gif created.  Saving index of converted video file")                                                                              
          with open('/data/device_tracking.db', mode='a') as db:                                                                                         
            dbo = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                                                          
            dbo.writerow(['doorbell', d, str(doorbells.last_recording_id)])                                                                        
          clearJpgCmd = "rm -f /data/doorbell"+str(d)+"*.jpg"                                                                               
          os.system(clearJpgCmd)  
          print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": New GIF generated: doorbell" + str(d) + ".gif")                                                                                                                        
        d=d+1 
    time.sleep(5)
  except NameError:
    print(datetime.datetime.now().replace(microsecond=0).isoformat() + ": Connecting to Ring.com.")
    myring = Ring(email, password)


#for chimes in myring.doorbells:
#for stickup_cams in myring.doorbells:

