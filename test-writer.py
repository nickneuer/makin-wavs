
from freq_writer import * 
import sys
from scipy.io import wavfile

#def main():

fl = './wavs/input/' + sys.argv[1]

rt, dat = wavfile.read(fl)
windows = make_windows(fl, 1024) 
freq_list = get_freqs(windows, rt)
freq_lu = freq_dict(windows, rt)
freq_zip = zip(freq_list, freq_list)
grps = np.array(group_by_threshold(freq_zip, 5))
grps = map(lambda x: x.T[0], grps)

data = []
used_freqs=[]
for grp in grps:
    try:
        freq = stats.mode(grp)[0][0]
        used_freqs.append(freq)
        data.append(freq_lu[freq][used_freqs.count(freq)-1])
    except IndexError:
        print freq, used_freqs.count(freq)-1

data = np.concatenate(data)

flname = './wavs/output/processed_' + sys.argv[1]

wavfile.write(flname, rt, data)

#if __name__ == '__main__':
#    main()


