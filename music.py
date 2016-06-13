
import numpy as np 

class NoteSample(object):
    def __init__(self, note, audio, sample_rate=44100):
        self.note = note
        self.audio = audio 
        self.sample_rate = sample_rate

    def __hash__(self):
        return hash(self.note)

    def __eq__(self, other):
        return self.note == other.note

    def __ne__(self, other):
        return not self == other

    def dump_audio(self, sinewave=False):
        if sinewave:
            A = np.max(self.audio)
            duration = len(self.audio)
            audio = nth_harmonic(self.note.to_frequency(), A, duration)
        else:
            audio = self.audio
        return audio


class Note():
    
    notes = ['A', 'Bb', 'B', 'C', 'Db', 'D','Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    # I know, I know. No microtonal support, so pedestrian.

    def __init__(self, pitch, octave):
        self.pitch = pitch 
        self.octave = octave

    def __hash__(self):
        return hash((self.pitch, self.octave))

    def __eq__(self, other):
        return (self.pitch == other.pitch) and (self.octave == other.octave)

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def from_degree(degree):
        return Note( Note.notes[degree % 12] , degree // 12 )

    @staticmethod
    def from_frequency(frequency):
        if frequency == 0:
            return Note(None, 0)
        else:
            return Note.from_degree(int(round(12 * np.log2(frequency / 440.0))))

    def __repr__(self):
        return "Note('{}', {})".format(self.pitch, self.octave)

    def to_degree(self):
        return Note.notes.index(self.pitch) + self.octave * 12

    def to_frequency(self):
        if self.pitch:
            return round(440 * np.power(np.power(2, 1 / 12.), self.to_degree()))
        else:
            return 0


def nth_harmonic(f, A, num_samples, n=1):
    w = 2 * np.pi * f
    rt = 44100
    tstep = 1./rt
    t = np.arange(num_samples) * tstep
    return np.array(A * np.sin(w * n * t), dtype='int16')