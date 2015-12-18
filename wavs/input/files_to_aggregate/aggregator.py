import os 
from scipy.io import wavfile
import numpy as np 

# drop in a directory of wav files and aggregate into one big one for 
# training markov chain on a bunch of different stuff 

def aggregate_files(): 
	data = []
	rate = 0
	for fl in filter(lambda x: x.lower().endswith('.wav'), os.listdir('.')): 
		rt, fileData = wavfile.read(fl)
		rate = rt                       # eh, whatever! 
		data.append(fileData)
    #
	allData = np.concatenate(data)
	#
	return rate, allData
	wavfile.write("aggregated_wavfiles.wav", rate, allData)


if __name__ == '__main__': 
	aggregate_files()



