from scipy import stats
import numpy as np
from scipy.io import wavfile
from freq_writer import *
import sys 

# fl = './wavs/input/scales_stuff.wav'
flnm = sys.argv[1]

windowSize = 1024 #int(sys.argv[2])

threshold = 5 #int(sys.argv[3])

filterLength = 1024 * 4 #int(sys.argv[4])


fl = flnm

rt, windows = rate_and_windows(fl, windowSize)

freqs = get_freqs(windows, rt)

freqsAndWindows = zip(freqs, windows)

groupedFreqs = group_by_threshold(freqsAndWindows, threshold)

freqs, data = map(lambda x: stats.mode(x)[0][0], map(lambda x: x.T[0], groupedFreqs)) \
			, map(np.concatenate, map(lambda x: x.T[1], groupedFreqs))

# data = map(np.concatenate, map(lambda x: x.T[1], groupedFreqs))

# data = filter(lambda x: x.size > filterLength, data)

freqWithData = zip(freqs, data)

zeros = np.zeros(rt/2, dtype='int16')

for freq, note in freqWithData: 
	print 'frequency: {0}     length: {1}'.format(freq, note.size)

out = []
for f, x in freqWithData:
	out.append(n_harm(f, 1, max(x), len(x))) #np.append(x * np.hanning(len(x)), zeros), dtype='int16') )

wavfile.write('./wavs/output/frequency_check.wav', rt, np.concatenate(out))




# map(lambda x: (x[1]), groupedFreqs[1])

# np.concatenate(map(lambda x: (x[1]), groupedFreqs[1]))