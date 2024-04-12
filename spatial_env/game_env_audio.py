from game_env import GameEnv

import numpy as np
from numpy import dot
from numpy.linalg import norm
import slab

import time

hrtf = slab.HRTF.kemar()
coords = hrtf.sources.cartesian[0]/1.399

# song_name = "Imagine Dragons - Warriors"
song_name = "Detective Conan - Hello Mr. My Yesterday 10기 오프닝(OP)"
# song_name = "Jacob Collier - Moon River"

bass = slab.Sound.read(f"./separated/htdemucs/{song_name}/bass.wav")
drums = slab.Sound.read(f"./separated/htdemucs/{song_name}/drums.wav")
other = slab.Sound.read(f"./separated/htdemucs/{song_name}/other.wav")
vocals = slab.Sound.read(f"./separated/htdemucs/{song_name}/vocals.wav")

# BASS_DIR   = np.array([0.0, 0.0, 0.0])
BASS_DIR   = np.array([0.0, 0.0, -0.4])
DRUMS_DIR  = np.array([0.0, 0.4, 0.0])
# OTHER_DIR  = np.array([0.0, 0.0, 0.0])
OTHER_DIR  = np.array([0.4, 0.0, 0.0])
VOCALS_DIR = np.array([0.0, -0.4, 0.0])

def direction_to_kemar_source(direction, kemar_hrtf):
    coords = kemar_hrtf.sources[0]/1.399
    cos_sim = dot(direction, coords.T)/(norm(direction)*norm(coords))
    idx = cos_sim.argmax()
    return idx


start_time = time.time()
prev_time = start_time

ge = GameEnv()
while True:
    res = ge.step()

    # print(ge.camera_rot)

    # duration = time.time() - prev_time
    duration = 1

    rel_prev_time = prev_time - start_time

    bass_buffer = bass.trim(rel_prev_time, rel_prev_time + duration)
    drums_buffer = drums.trim(rel_prev_time, rel_prev_time + duration)
    other_buffer = other.trim(rel_prev_time, rel_prev_time + duration)
    vocals_buffer = vocals.trim(rel_prev_time, rel_prev_time + duration)
    # spatial_sounds[0].trim(0, 0.01)

    # rel_bass_dir = ge.camera_rot @ BASS_DIR
    # rel_drums_dir = ge.camera_rot @ DRUMS_DIR
    # rel_other_dir = ge.camera_rot @ OTHER_DIR
    # rel_vocals_dir = ge.camera_rot @ VOCALS_DIR
    # rel_bass_dir = ge.camera_rot @ np.roll(BASS_DIR, 1)
    # rel_drums_dir = ge.camera_rot @ np.roll(DRUMS_DIR, 1)
    # rel_other_dir = ge.camera_rot @ np.roll(OTHER_DIR, 1)
    # rel_vocals_dir = ge.camera_rot @ np.roll(VOCALS_DIR, 1)
    # rel_bass_dir = np.roll(ge.camera_rot @ np.roll(BASS_DIR, 1), -1)
    # rel_drums_dir = np.roll(ge.camera_rot @ np.roll(DRUMS_DIR, 1), -1)
    # rel_other_dir = np.roll(ge.camera_rot @ np.roll(OTHER_DIR, 1), -1)
    # rel_vocals_dir = np.roll(ge.camera_rot @ np.roll(VOCALS_DIR, 1), -1)
    # rel_bass_dir = np.roll(ge.camera_rot.T @ np.roll(BASS_DIR, 2), -2)
    # rel_drums_dir = np.roll(ge.camera_rot.T @ np.roll(DRUMS_DIR, 2), -2)
    # rel_other_dir = np.roll(ge.camera_rot.T @ np.roll(OTHER_DIR, 2), -2)
    # rel_vocals_dir = np.roll(ge.camera_rot.T @ np.roll(VOCALS_DIR, 2), -2)
    rel_bass_dir = np.roll(ge.camera_rot @ np.roll(BASS_DIR, 2), -2)
    rel_drums_dir = np.roll(ge.camera_rot @ np.roll(DRUMS_DIR, 2), -2)
    rel_other_dir = np.roll(ge.camera_rot @ np.roll(OTHER_DIR, 2), -2)
    rel_vocals_dir = np.roll(ge.camera_rot @ np.roll(VOCALS_DIR, 2), -2)

    bass_idx = direction_to_kemar_source(rel_bass_dir, hrtf)
    drums_idx = direction_to_kemar_source(rel_drums_dir, hrtf)
    other_idx = direction_to_kemar_source(rel_other_dir, hrtf)
    vocals_idx = direction_to_kemar_source(rel_vocals_dir, hrtf)
    print(vocals_idx)

    # bass_spatial = hrtf.apply(bass_idx, bass)
    # drums_spatial = hrtf.apply(drums_idx, drums)
    # other_spatial = hrtf.apply(other_idx, other)
    # vocals_spatial = hrtf.apply(vocals_idx, vocals)
    bass_spatial = hrtf.apply(bass_idx, bass_buffer)
    drums_spatial = hrtf.apply(drums_idx, drums_buffer)
    other_spatial = hrtf.apply(other_idx, other_buffer)
    vocals_spatial = hrtf.apply(vocals_idx, vocals_buffer)

    combined = bass_spatial + drums_spatial + other_spatial + vocals_spatial

    combined.play()

    # ge.camera_yaw
    # ge.camera_pitch

    prev_time = time.time()

    if res == "END": 
        ge.end()
        break
