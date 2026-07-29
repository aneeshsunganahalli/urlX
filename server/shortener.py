import time
CUSTOM_EPOCH=1785176805

from threading import Lock

mutex = Lock()

# 4 bit field for Workers, maually provide through docker/env of each instance
w = 8

# 12 bit for sequencing
lts = 0
seq = 0

mutex.acquire()
# On request
cts = int(time.time()) - CUSTOM_EPOCH
if cts == lts:
  if seq == 4095:
    now = time.time()
    wait_time = 1.0 - (now % 1.0)
    time.sleep(wait_time)
    
    cts = int(time.time()) - CUSTOM_EPOCH
    lts = cts
    seq = 0
  else:
    seq += 1
  
else:
  seq = 0
  lts = cts



# ts | worker id | seq
id = cts << 16 | w << 12 | seq
print(id)

mutex.release()

import base62

encoded_id = base62.encode(id)
print(encoded_id)






