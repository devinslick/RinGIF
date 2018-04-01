#!/usr/bin/python
import sys
from ring_doorbell import Ring
myring = Ring(sys.argv[1], sys.argv[2])
doorbell = myring.doorbells[0]
print(doorbell.recording_url(doorbell.last_recording_id))
doorbell.recording_download(doorbell.history(limit=100)[0]['id'],filename='www/videos/last_recording.mp4',override=True)

