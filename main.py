from ring_doorbell import Ring
import os
import csv
import time
import ffmpeg
import wget
 
email = str(os.environ['email'])
password = str(os.environ['password'])
resolution = str(os.environ['resolution'])
fps = str(os.environ['fps'])

def isLatest(recordingID):                                                              
  if os.path.exists('device_tracking.db'):
    with open('device_tracking.db', 'rt') as f:                                           
      reader = csv.reader(f, delimiter=',')                                               
      for row in reader:                                                                  
        if str(recordingID) == row[2]:                                                    
          return "true"                                                                   
      return "false" 
  else:
    with open('device_tracking.db', 'w+') as db:
      db.write('DeviceType,DeviceID,RecordingID\n')
    return "false"

os.system("rm -f /data/*.jpg")  

while True:
  try:
    if myring.is_connected != True:
      print("Existing Ring.com connection has timed out, reconnecting...")
      myring = Ring(email, password)
    if myring.is_connected == True:
      print("Ring.com connection is healthy.")
      d=0                                                                 
      for doorbells in myring.doorbells:                                  
        if isLatest(doorbells.last_recording_id) == 'true':               
          print "Doorbell " + str(d) + ", recording " + str(doorbells.last_recording_id) + " was already saved."                                                                 
        else:                                                                                                         
          print("Getting recording URL for doorbell #" + str(d) + ". RecordingID: " + str(doorbells.last_recording_id) )
          print(myring.is_connected)
          url=str(doorbells.recording_url(doorbells.last_recording_id))                                            
          if "https" not in url:
            print("Invalid URL returned.  Exiting")
            sys.exit(1)
          print(url)
          print('Starting download for doorbell #' + str(d) + '. Recording: ' + str(doorbells.last_recording_id) )                                 
          wgetCmd = 'wget -O /data/doorbell'+str(d)+'.mp4 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2460.41 Safari/537.36" "'+url+'"' 
          os.system(wgetCmd)                                                                                                                        
          print("Download complete, starting ffmpeg")                                                                                               
          (                                                                                                                                         
            ffmpeg                                                                                                                                  
            .input("/data/doorbell"+str(d)+".mp4")                                                                                                  
            .filter('fps', fps=fps, round='up')                                                                                                       
            .output("/data/doorbell"+str(d)+"-%03d.jpg")                                                                                            
            .run()                                                                                                                                  
          )                                                                                                                                         
          print("ffmpeg complete, starting jpeg optimization")                                                                                      
          jpgCmd = "jpegoptim -f -q -s /data/doorbell"+str(d)+"*.jpg"                                                                               
          os.system(jpgCmd)                                                                                                                         
          print("jpeg optimization complete, creating gif")                                                                                         
          gifCmd = "convert -delay 20 -loop 0 /data/doorbell"+str(d)+"*.jpg -resize " + resolution + " /data/doorbell" + str(d) + ".gif"                 
          os.system(gifCmd)                                                               
          print("gif created.  Saving index of converted video file")                                                                              
          with open('device_tracking.db', mode='a') as db:                                                                                         
            dbo = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)                                                          
            dbo.writerow(['doorbell', d, str(doorbells.last_recording_id)])                                                                        
          clearJpgCmd = "rm -f /data/doorbell"+str(d)+"*.jpg"                                                                               
          os.system(clearJpgCmd)  
          print("New GIF generated: doorbell" + str(d) + ".gif")                                                                                                                        
        d=d+1 
    time.sleep(5)
  except NameError:
    print("Connecting to Ring.com.")
    myring = Ring(email, password)


#for chimes in myring.doorbells:
#for stickup_cams in myring.doorbells:

