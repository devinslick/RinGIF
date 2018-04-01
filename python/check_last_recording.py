#!/usr/bin/python
import sys
from ring_doorbell import Ring
myring = Ring(sys.argv[1], sys.argv[2])
doorbell = myring.doorbells[0]
f= open("variables/recording.current","w+")
f.write(doorbell.recording_url(doorbell.last_recording_id))
f.close()
