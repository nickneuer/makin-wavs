import os
from markov_dict import MarkovDict
from freq_writer import * 
from scipy.io import wavfile
import sys 

if not os.path.isdir("./wavs/output"):
    os.path.makedirs("./wavs/output")

fl = sys.argv[1]
ngram_size = int(sys.argv[2])
duration = int(sys.argv[3])

# python nunu_shredder.py Faster_licks.wav 4 150
 
flname = './wavs/input/' + fl 

#rt, data = wavfile.read(flname)

#windows = make_windows(flname, 1024)

#mk = MarkovDict(windows, rt, ngram_size)

mk = MarkovDict(ngram_size, window_size=1024, filter_length=4096, threshold=10)

outfile = 'processed_' + fl

#mk.write_licks(duration, outfile)  

mk.write_licks(flname, duration, outfile)

