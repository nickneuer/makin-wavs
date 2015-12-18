from scipy import stats
import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt

# fl = './wavs/input/scales_stuff.wav'

# rt, dat = wavfile.read(fl)

def make_windows(fl, length):
    rate, data = wavfile.read(fl)
    data = data.T[0]
    return np.array_split(data, data.size/float(length))
    
def rate_and_windows(fl, length):
    rate, data = wavfile.read(fl)
    windows = make_windows(fl, length)
    return rate, windows

def rolling_modes(freqs):
    modes = map(lambda n: stats.mode(freqs[n-1 : n + 3])[0][0], np.arange(1, len(freqs) - 2))
    return modes

def get_freqs(windows, rate, window_size=1024, threshold=5): 
    # returns a list of frequencies corresponding to each window
    # windows an array of np arrays
    hanning_windows = [np.hanning(len(window))*window for window in windows]
    padding = np.zeros(window_size)
    padded_windows = map(lambda window: np.append(window, padding), hanning_windows) 
    fourier = [np.fft.fft(window) for window in padded_windows] # hanning_windows] 

    the_freqs = [np.fft.fftfreq(len(window)) for window in fourier]
    filtered_freqs = []
    for coeffs, freqs in zip(fourier, the_freqs):
        #idx = np.argmax(np.abs(coeffs))
        idx = np.argmax(np.abs(coeffs))
        #max_freq = rate * freqs[idx]
        max_freq = abs(rate * freqs[idx]) # unsure if abs should be used here
        filtered_freqs.append(max_freq)
    modes = rolling_modes(rolling_modes(filtered_freqs))
    return normalize_freq_list(modes, threshold)

def plot_freqs(fl):
    rt = wavfile.read(fl)[0]
    windows = make_windows(fl, 1024)
    freqs = get_freqs(windows, rt)
    plt.plot(freqs, 'ro')
    plt.show()


def group_by_threshold(li, threshold):
    # to group similar frequencies into same note
    # the transpose and all of that voodo is so it only groups by differences in first 
    # coordinate
    li = np.array(li, dtype='O')
    return np.split(li, np.where(np.abs(np.diff(li.T[0])) > threshold)[0]+1)

def normalize_freq_list(freq_list, threshold):
    sorted_freqs = sorted(freq_list)
    key_choices = np.split(sorted_freqs, np.where(np.abs(np.diff(sorted_freqs)) > threshold)[0] + 1)
    key_lkp = {}
    for arr in key_choices:
        for elt in arr:
            val = arr[0]
            key_lkp[elt] = val
    return map(lambda f: key_lkp[f], freq_list) 

def freq_dict(windows, rate, threshold=5):
    freq_lu = dict()
    #hanning_windows = [np.hanning(len(window))*window for window in windows]
    the_freqs = get_freqs(windows, rate, threshold)
    # wanna zip up each freq with the data window that birthed it in a tuple
    freqs_and_windows = np.array(zip(the_freqs, windows), dtype='O')
    for group in group_by_threshold(freqs_and_windows, 0):
        group = np.array(group, dtype='O')
        freq_key = group.T[0][0]
        if freq_key not in freq_lu: 
            freq_lu[freq_key] = [np.int16(np.concatenate(group.T[1]))]
            # groups together data which produces this frequency as value for freq_key
        else:
            freq_lu[freq_key].append(np.int16(np.concatenate(group.T[1])))

    return freq_lu

def smooth_onset(signal):
    return np.array(np.hanning(len(signal) ) * signal, dtype='int16') 

def check_freqs(freq_list):
    data = [0]
    for freq in freq_list:
        data = np.append(data, freq)
        data = np.array(data, dtype='int16')
    wavfile.write('test.wav', 44100, data)



