
import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt
from spectrum import Fft, Shc, Spectrum
from music import Note, NoteSample
import pyaudio

class AudioSample(object):
    
    def __init__(self, rate, samples):
        if len(np.shape(samples)) > 2:
            raise ValueError("More than 2 channels in audio file.")
        self.rate = rate
        self.samples = samples
        self.channels = len(np.shape(samples))

    @staticmethod
    def from_wav(fname):
        return AudioSample(*wavfile.read(fname))

    def left_channel(self):
        return self._get_channel(0)

    def right_channel(self):
        return self._get_channel(1)

    def _get_channel(self, i):
        if len(np.shape(self.samples)) == 1:
            return self
        else:
            return AudioSample(self.rate, self.samples[:,i])

    def windows(self, window_size=1024 * 4, offset=1024 * 2):
        return WindowedSample(self, window_size, offset)

    def plot(self):
        if len(np.shape(self.samples)) > 1:
            raise ValueError("cannot plot AudioSample with more than 1 channel")
        else:
            plt.plot(self.samples)
            plt.show()

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, output=1)
        stream.write(self.samples)
        stream.close()


class WindowedSample(object):

    def __init__(self, sample, window_size=1024 * 4, offset=1024 * 2):
        self.rate = sample.rate
        self.window_size = window_size
        self.offset = offset
        self.windows = WindowedSample._create_windows(sample, window_size, offset)

    @staticmethod
    def _create_windows(sample, window_size, offset):
        windows = []
 
        diff = window_size - (np.shape(sample.samples)[0] % window_size)
        audiosample = np.append(sample.samples, np.zeros(diff)) 
        first = np.split(audiosample
            , np.where(np.arange(len(audiosample)) % window_size == 0)[0][1:])

        second = np.split(audiosample[offset:len(audiosample) - offset]
            , np.where(np.arange(len(audiosample) - offset) % window_size == 0)[0][1:])

        for n in xrange(len(second) - 1):
            windows.append(Window(window_size, first[n], sample.rate))
            windows.append(Window(window_size, second[n], sample.rate))
        windows.append(Window(window_size, first[-1], sample.rate))
        return windows

    def to_training_notes(self, transform=Fft, **transform_args):

        def unpack_windows(windows):
            return np.array(
                np.concatenate(
                    map(lambda w: w.samples[:self.offset], windows )
                ), dtype='int16')  

        notes = np.array(map(lambda w: w.get_note(transform, **transform_args), self.windows))
        note_switches = np.where(np.abs(
            np.diff(
                np.array(map(lambda n: n.to_frequency(), notes))
                )
            ) > 0)[0] + 1
        return [NoteSample(notes[0], unpack_windows(windows), self.rate) for notes, windows in \
            zip(np.split(notes, note_switches), np.split(self.windows, note_switches))]


class Window(object):

    def __init__(self, window_size, samples, rate):
        self.window_size = window_size
        self.samples = samples
        self.rate = rate

    def hanning(self):
        return Window(
            self.window_size,
            np.hanning(self.window_size) * self.samples,
            self.rate)

    def plot(self):
        plt.plot(self.samples)
        plt.show()

    def plot_spectrum(self, transform=Fft, **transform_args):
        transform(self.samples, **transform_args).plot()

    def get_freq(self, transform=Fft, **transform_args):
        return round(transform(self.samples, **transform_args).get_freq(), 1)

    def get_note(self, transform=Fft, **transform_args):
        freq = self.get_freq(transform, **transform_args)
        return Note.from_frequency(freq)


if __name__ == '__main__':
    
    f = './wavs/input/scales_stuff.wav'

    a = AudioSample.from_wav(f)

    windows = a.windows().windows

