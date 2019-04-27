from ring_doorbell import Ring
import osi
destPath = '/data/' + os.environ['vidName']
myring = Ring(os.environ['email'], os.environ['password'])
doorbell = myring.doorbells[0]
recordingID=str(doorbell.last_recording_id)
with open('/data/previous.recording', 'r') as recording:
  old = str(recording.read())
recording.close()
if old != recordingID:
  print("Updates")
  doorbell = myring.doorbells[0]
  doorbell.recording_download(doorbell.history(limit=100)[0]['id'],filename=destPath,override=True)
  with open('/data/previous.recording', 'w') as tracker:
    tracker.write(recordingID)
  tracker.close()
else:
  print("Nothing")
