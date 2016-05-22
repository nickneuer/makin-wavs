
from matplotlib import pyplot as plt 
import numpy as np
from scipy.io import wavfile

from freq_writer import * 

fl = './wavs/input/scales_stuff.wav'

windows = make_windows(fl, 1024)


class Spectrum(object):
	#
	def __init__(self, freqs=[0], coeffs=[0]):
		self.freqs = freqs
		self.coeffs = coeffs
	#
	def plot(self):
		plt.plot(self.freqs, self.coeffs)
		plt.show()
	#
	def get_freq(self):
		idx = np.argmax(self.coeffs)
		f = self.freqs[idx]
		return f

class Fft(Spectrum):
	#
	def __init__(self, fft_samples=1024, rt=44100, freqs=[0], coeffs=[0]):
		self.fft_samples = fft_samples
		self.rt = rt
	#
	def apply(self, window):
		self.coeffs = np.abs(np.fft.rfft(np.hanning(len(window)) * window, self.fft_samples))
		self.freqs = np.fft.rfftfreq(self.fft_samples) * self.rt


class Shc(Spectrum):
	#
	def __init__(self, fft_samples=1024, nharm=3, wl=40, fmin=70, fmax=1300, rt=44100, freqs=[0], coeffs=[0]): #, freqs=[0], coeffs=[0]):
		self.fft_samples = fft_samples
		self.nharm = nharm
		self.wl = wl
		self.fmin = fmin
		self.fmax = fmax
		self.rt = rt
		self.freqs=freqs
		self.coeffs=coeffs
	#
	def apply(self, window):
		f, v = shc(window, fft_samples=self.fft_samples, nharm=self.nharm, wl=self.wl, fmin=self.fmin,
			fmax=self.fmax, rt=self.rt)
		self.freqs = f
		self.coeffs = v
	#

	
def shc(window, fft_samples=1024, nharm=3, wl=40, fmin=70, fmax=1300, rt=44100):
    enveloped = np.hanning(len(window)) * window
    spectrum = np.abs(np.fft.rfft(enveloped, fft_samples))
    freqs = np.fft.rfftfreq(fft_samples) * rt
    filtered_idxs = np.where((freqs >= fmin) & (freqs <= fmax))[0]
    freqstep = float(rt) / fft_samples # freq change in Hz for each index into freqs
    step_size = int((wl/2.) / freqstep)
    def shc_n(n):
        harms = np.arange(1, nharm + 2)
        shcn = 0
        for f in xrange(-1 * step_size, step_size + 1):
            if n + f < 0:
                prod = 0
            else:
                prod = np.prod(spectrum[ n * harms + f])
            shcn += prod
        return shcn
    shc_values = freqs[filtered_idxs], map(shc_n, filtered_idxs)
    return shc_values


