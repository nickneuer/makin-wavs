
import numpy as np
from scipy.io import wavfile

fl = './wavs/input/scales_stuff.wav'

rt, dat = wavfile.read(fl)

def make_windows(fl, length):
    rate, data = wavfile.read(fl)
    data = data.T[0]
    return np.array_split(data, data.size/float(length))
    
def get_freqs(windows, rate):
    # windows an array of np arrays
    fourier = [np.fft.fft(window) for window in windows] 
    the_freqs = [np.fft.fftfreq(len(window)) for window in fourier]
    filtered_freqs = []
    for coeffs, freqs in zip(fourier, the_freqs):
        idx = np.argmax(np.abs(coeffs))
        #max_freq = rate * freqs[idx]
        max_freq = abs(rate * freqs[idx])
        filtered_freqs.append(max_freq)
    return filtered_freqs

def freq_dict(windows, rate):
    # windows an array of np arrays
    fourier = [np.fft.fft(window) for window in windows] 
    the_freqs = [np.fft.fftfreq(len(coeffs)) for coeffs in fourier]
    freq_lu = dict()
    for coeffs, freqs in zip(fourier, the_freqs):
        idx = np.argmax(np.abs(coeffs)) 
        max_freq = abs(rate * freqs[idx])
        if max_freq not in freq_lu:
            coeffs = np.fft.ifft(coeffs)
            freq_lu[max_freq]=np.int16(np.real(coeffs))
    return freq_lu

def group_by_threshold(li, threshold):
    # to group similar frequencies into same note
    return np.split(li, np.where(abs(np.diff(li)) > threshold)[0]+1)
         
    
