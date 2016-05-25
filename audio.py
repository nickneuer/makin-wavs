import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt

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

    def windows(self, win_size, overlap):
        return WindowedSample(self, win_size, overlap)

    def plot(self):
        if len(np.shape(self.samples)) > 1:
            raise ValueError("cannot plot AudioSample with more than 1 channel")
        else:
            plt.plot(self.samples)
            plt.show()


class WindowedSample(object):

    def __init__(self, sample, window_size, overlap):
        self.rate = sample.rate
        self.window_size = window_size
        self.overlap = overlap
        self.windows = _create_windows(sample, window_size)

    @staticmethod
    def _create_windows(sample, window_size, overlap):
        pass
        

class Window(object):

    def __init__(self, window_size, samples, rate):
        self.window_size = window_size
        self.samples = samples

    def hanning(self):
        return Window(
            self.window_size,
            np.hanning(self.window_size) * self.samples,
            self.rate)

    def plot(self):
        plt.plot(self.samples)
        plt.show()

