import numpy as np
from numpy import dot
from numpy.linalg import norm
import slab
from spatial_env.head_tracker import HeadTracker

hrtf = slab.HRTF.kemar()
coords = hrtf.sources.cartesian[0]/1.399

ht = HeadTracker()

ht.start()
while True:
    res = ht.step()
    if res == -1: break
ht.end()

