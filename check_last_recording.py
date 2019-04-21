from ring_doorbell import Ring
import os
import requests
myring = ''
new=''
doorbell=''
myring = Ring(os.environ['email'], os.environ['password'])
doorbell = myring.doorbells[0]
recordingID=str(doorbell.last_recording_id)
with open('/data/previous.recording', 'r') as recording:
  old = str(recording.read())
if old != recordingID:
  print("Updates")
  r = requests.get(doorbell.recording_url(recordingID))
  with open('/data/last_recording.mp4', 'wb') as f:
    f.write(r.content)
  f.close()
  f= open("/data/previous.recording","w+")
  f.write(str(recordingID))
  f.close()
else:
  print("Nothing")
