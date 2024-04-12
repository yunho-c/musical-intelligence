from game_env import GameEnv

import numpy as np
from numpy import dot
from numpy.linalg import norm
import slab

import time

hrtf = slab.HRTF.kemar()
coords = hrtf.sources.cartesian[0]/1.399

song_name = "Imagine Dragons - Warriors"
# song_name = "Detective Conan - Hello Mr. My Yesterday 10기 오프닝(OP)"
# song_name = "Jacob Collier - Moon River"

bass = slab.Sound.read(f"./separated/htdemucs/{song_name}/bass.wav")
drums = slab.Sound.read(f"./separated/htdemucs/{song_name}/drums.wav")
other = slab.Sound.read(f"./separated/htdemucs/{song_name}/other.wav")
vocals = slab.Sound.read(f"./separated/htdemucs/{song_name}/vocals.wav")

BASS_DIR = [0.0, 0.0, 0.0]
DRUMS_DIR = [0.0, 0.4, 0.0]
OTHER_DIR = [0.0, 0.0, 0.0]
VOCALS_DIR = [0.0, -0.4, 0.0]

def direction_to_kemar_source(direction, kemar_hrtf):
    coords = kemar_hrtf.sources[0]/1.399
    cos_sim = dot(direction, coords.T)/(norm(direction)*norm(coords))
    idx = cos_sim.argmax()
    return idx




ge = GameEnv()
while True:
    res = ge.step()


    ge.camera_yaw
    # ge.camera_pitch

    if res == "END": 
        ge.end()
        break
