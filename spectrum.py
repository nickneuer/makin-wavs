
from matplotlib import pyplot as plt 
import numpy as np
from scipy.io import wavfile 


class Spectrum(object):
    def __init__(self):
        self._apply()

    def plot(self):
        plt.plot(self.freqs, self.coeffs)
        plt.show()

    def get_freq(self):
        return self.freqs[np.argmax(self.coeffs)]


class Fft(Spectrum):
    
    def __init__(self, window, fft_samples=1024*2, fmin=70, fmax=1300, rt=44100):
        self.fft_samples = fft_samples
        self.rt = rt
        self.window = window
        self.fmin = fmin
        self.fmax = fmax
        super(Fft, self).__init__()

    def _apply(self):
        coeffs = np.abs(np.fft.rfft(np.hanning(len(self.window)) * self.window, self.fft_samples))
        freqs = np.fft.rfftfreq(self.fft_samples) * self.rt
        filtered_idxs = np.where((freqs >= self.fmin) & (freqs <= self.fmax))[0]
        self.coeffs, self.freqs = coeffs[filtered_idxs], freqs[filtered_idxs]


class Shc(Spectrum):
    def __init__(self, window, fft_samples=1024*2, nharm=3, wl=40, fmin=70, fmax=1300, rt=44100):
        self.fft_samples = fft_samples
        self.nharm = nharm
        self.wl = wl
        self.fmin = fmin
        self.fmax = fmax
        self.rt = rt
        self.window = window
        super(Shc, self).__init__()

    def _apply(self):
        enveloped = np.hanning(len(self.window)) * self.window
        spectrum = np.abs(np.fft.rfft(enveloped, self.fft_samples))
        freqs = np.fft.rfftfreq(self.fft_samples) * self.rt
        filtered_idxs = np.where((freqs >= self.fmin) & (freqs <= self.fmax))[0]
        freqstep = float(self.rt) / self.fft_samples # freq change in Hz for each index into freqs
        step_size = int((self.wl/2.) / freqstep)
        def shc_n(n):
            harms = np.arange(1, self.nharm + 2)
            shcn = 0
            for f in xrange(-1 * step_size, step_size + 1):
                if n + f < 0:
                    prod = 0
                else:
                    prod = np.prod(spectrum[ n * harms + f])
                shcn += prod
            return shcn
        self.freqs, self.coeffs = freqs[filtered_idxs], map(shc_n, filtered_idxs)
