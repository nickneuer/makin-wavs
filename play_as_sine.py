import numpy as np
from note_lookup import Note
import sys
from freq_writer import check_freq
from audio import * 
from scipy.io import wavfile

win_size = int(sys.argv[2])
fft_samples = int(sys.argv[3])

f = sys.argv[1] #'./wavs/input/C_Major.wav'
rate, _ = wavfile.read(f)

windows = AudioSample.from_wav(f).left_channel().windows(win_size=1024*2).windows
notes = np.array(map(lambda w: w.get_note(fft_samples=1024*4, rt=rate), windows))
note_switches = np.where(np.abs(np.diff(np.array(map(lambda n: n.to_frequency(), notes)))) > 0)[0] + 1
notes_and_windows = zip(np.split(notes, note_switches), np.split(windows, note_switches))
final = [(note_arr[0], np.array(np.concatenate(map(lambda w: w.samples[:len(w.samples)/2], window_arr)), dtype='int16')) \
	for note_arr, window_arr in notes_and_windows]

for note, sample in final:
	if len(sample) > 1024 * 5:
		check_freq(note.to_frequency(), 2 * len(sample))
		# check_audio(sample)
