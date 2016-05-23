import numpy as np
from scipy.io import wavfile

class AudioSample(object):
    def __init__(self, rate, samples):
        if len(np.shape(samples)) > 2:
            raise ValueError("More than 2 channels in audio file.")
        self.rate = rate
        self.samples = samples

    @staticmethod
    def from_wav(fname):
        return AudioSample(*wavfile.read(fname))

    def left_channel(self):
        self._get_channel(0)

    def right_channel(self):
        self._get_channel(1)

    def _get_channel(self, i):
        if len(np.shape(self.samples)) == 1:
            return self.samples
        else:
            return self.samples[:,i]

    def windows(self, win_size):
        return WindowedSample(self, win_size)

    def plot(self):
        pass


class WindowedSample(object):
    def __init__(self, sample, window_size):
        self.rate = sample.rate
        self.window_size = window_size
        self.windows = _create_windows(sample, window_size)

    def plot(self):
        pass

    @staticmethod
    def _create_windows(sample, window_size):
        pass


class Window(object):
    def __init__(self):
        pass

    def hanning(self):
        pass
