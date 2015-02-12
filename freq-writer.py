from scipy import stats
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

def group_by_threshold(li, threshold):
    # to group similar frequencies into same note
    # the transpose and all of that voodo is so it only groups by differences in first 
    # coordinate
    li = np.array(li, dtype='O')
    return np.split(li, np.where(abs(np.diff(li.T[0])) > threshold)[0]+1)


def freq_dict(windows, rate, threshold=5):
    freq_lu = dict()
    the_freqs = get_freqs(windows, rate)
    # wanna zip up each freq with the data window that birthed it in a tuple
    freqs_and_windows = np.array(zip(the_freqs, windows), dtype='O')
    for group in group_by_threshold(freqs_and_windows, threshold):
        group = np.array(group, dtype='O')
        freq_key = stats.mode(group.T[0])[0][0]
        if freq_key not in freq_lu: 
            freq_lu[freq_key] = [np.int16(np.concatenate(group.T[1]))]
            # groups together data which produces this frequency as value for freq_key
        else:
            freq_lu[freq_key].append(np.int16(np.concatenate(group.T[1])))
        # don't want the values to be concatenated when different groups have same freq_key
        # need condition to prevent this 
    return freq_lu

        
    
