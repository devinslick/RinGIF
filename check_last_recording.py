from ring_doorbell import Ring
import os
import requests
print("Authenticating")
myring = ''
new=''
doorbell=''
myring = Ring(os.environ['email'], os.environ['password'])
doorbell = myring.doorbells[0]
recordingID=str(doorbell.last_recording_id)
print(recordingID)
with open('/data/previous.recording', 'r') as recording:
  old = str(recording.read())

if old != recordingID:
  print("different")
  print(str(recordingID))
  print(old)
  r = requests.get(doorbell.recording_url(recordingID))
  print('1')
  with open('/data/file.mp4', 'wb') as f:
    f.write(r.content)
  f.close()
  f= open("/data/previous.recording","w+")
  f.write(str(recordingID))
  f.close()
