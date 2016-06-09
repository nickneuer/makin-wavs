
import numpy as np 
from freq_writer import nth_harmonic 

class NoteAudio(object):
    def __init__(self, note, audio, sample_rate=44100):
        self.note = note
        self.audio = audio 
        self.sample_rate = sample_rate

    def dump_audio(self, sinewave=False):
        if sinewave:
            A = np.max(self.audio)
            duration = len(self.audio)
            audio = nth_harmonic(self.note.to_frequency(), A, duration)
        else:
            audio = self.audio
        return audio

