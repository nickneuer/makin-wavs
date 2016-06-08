from scipy import stats
import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt
from numpy.lib.stride_tricks import as_strided
import pyaudio

# fl = './wavs/input/scales_stuff.wav'

# rt, dat = wavfile.read(fl)

def normalize_freqs(freqs, threshold):
    ordered = sorted(freqs)
    val = ordered[0]
    freq_lu = {}
    for freq in ordered:
        if freq - val < threshold:
            freq_lu[freq] = val
        else:
            val = freq
            freq_lu[freq] = val
    return map(lambda f: freq_lu[f], freqs) 

def windowed_view(arr, window, overlap):
    arr = np.asarray(arr)
    window_step = window - overlap
    new_shape = arr.shape[:-1] + ((arr.shape[-1] - overlap) // window_step,
                                  window)
    new_strides = (arr.strides[:-1] + (window_step * arr.strides[-1],) +
                   arr.strides[-1:])
    return as_strided(arr, shape=new_shape, strides=new_strides)

def make_windows(fl, length):
    rate, data = wavfile.read(fl)
    overlap = length / 2
    if len(np.shape(data)) > 1:
        data = data.T[0]
    return windowed_view(data, length, overlap) # np.array_split(data, data.size/float(length))
    
def rate_and_windows(fl, length):
    rate, data = wavfile.read(fl)
    windows = make_windows(fl, length)
    return rate, windows

def rolling_modes(freqs):
    modes = map(lambda n: stats.mode(freqs[n-1 : n + 3])[0][0], np.arange(1, len(freqs) - 2))
    return modes

def get_freqs(windows, rate=44100, window_size=1024, threshold=5): 
    # returns a list of frequencies corresponding to each window
    # windows an array of np arrays
    hanning_windows = [np.hanning(len(window))*window for window in windows]
    padding = np.zeros(window_size)
    padded_windows = map(lambda window: np.append(window, padding), hanning_windows) 
    fourier = [np.fft.rfft(window) for window in padded_windows] # hanning_windows] 
    the_freqs = [np.fft.rfftfreq(len(window)) for window in fourier]
    filtered_freqs = []
    for coeffs, freqs in zip(fourier, the_freqs):
        #idx = np.argmax(np.abs(coeffs))
        idx = np.argmax(np.abs(coeffs))
        #max_freq = rate * freqs[idx]
        max_freq = abs(rate * freqs[idx]) # unsure if abs should be used here
        filtered_freqs.append(max_freq)
    modes = rolling_modes(filtered_freqs)
    return normalize_freqs(modes, threshold)

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

def get_freq_info(window):
    'returns (coeffs, freqs) tuple'
    hanning = np.hanning(len(window)) * window
    fourier = np.fft.rfft(window)
    freqs = np.fft.rfftfreq(len(window))
    return fourier, freqs

def top_n_freqs(window, n, rt=44100):
    coeffs, freqs = get_freq_info(window)
    n_max_idx = np.argsort(-coeffs)[:n + 2]
    max_freqs = [rt * freqs[idx] for idx in n_max_idx]
    return max_freqs[2:]

# n max: np.argsort(-arr)[:n]

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


def freq_dict(windows, rate, threshold=5):
    freq_lu = dict()
    #hanning_windows = [np.hanning(len(window))*window for window in windows]
    the_freqs = get_freqs(windows, rate, threshold)
    # wanna zip up each freq with the data window that birthed it in a tuple
    freqs_and_windows = np.array(zip(the_freqs, windows), dtype='O')
    groups = group_by_threshold(freqs_and_windows, 0)
    filtered = filter(lambda a: np.size(a) >= 5, groups)
    for group in group_by_threshold(freqs_and_windows, 0):
        group = np.array(group, dtype='O')
        freq_key = group.T[0][0]
        halfs = [a[0: np.size(a)/2] for a in group.T[1]]
        if freq_key not in freq_lu: 
            freq_lu[freq_key] = [np.int16(np.concatenate(halfs))]
            # groups together data which produces this frequency as value for freq_key
        else:
            freq_lu[freq_key].append(np.int16(np.concatenate(halfs)))
    return freq_lu

def smooth_onset(signal):
    return np.array(np.hanning(len(signal) ) * signal, dtype='int16') 

def nth_harmonic(f, A, num_samples, n=1):
    w = 2 * np.pi * f
    rt = 44100
    tstep = 1./rt
    t = np.arange(num_samples) * tstep
    return np.array(A * np.sin(w * n * t), dtype='int16')

def check_audio(audio_data):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=1)
    stream.write(audio_data)
    stream.close()

def play_windows(windows, start, stop):
    windows = windows[start:stop]
    data = [w.samples[:len(w.samples)/2] for w in windows] # get first half of each, since they're overlapped
    data = np.array(np.concatenate(data), dtype='int16')
    check_audio(data)

def check_freq(f, length=1024 * 50):
    data = nth_harmonic(f, 1, 15456, length)
    check_audio(data)



