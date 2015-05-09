
from freq_writer import * 
import sys
from scipy.io import wavfile
import random 

class MarkovDict(object):
    def __init__(self, windows, rate, prefix_length):
        self.windows = windows
        self.prefix_length = prefix_length
        self.rate = rate
        self.freq_dict = freq_dict(self.windows, self.rate)

    def list_freqs(self):
        freq_list = get_freqs(self.windows, self.rate)
        freq_zip = zip(freq_list, freq_list)
        grps = np.array(group_by_threshold(freq_zip, 5))
        grps = map(lambda x: x.T[0], grps)
        grps = map(list, grps)
        freqs = map(lambda grp: stats.mode(grp)[0][0], grps)
        return freqs

    def make_prefixes(self):
        freq_list = self.list_freqs()
        return map(lambda n: freq_list[n-self.prefix_length: n], range(self.prefix_length,len(freq_list)+1))
        
    def make_dict(self):
        prefixes = self.make_prefixes()     
        phrase_dict = dict() 
        for n, prefix in enumerate(prefixes):
          prefix = tuple(prefix)
          if n < len(prefixes)-1:
            if prefix in phrase_dict: 
              phrase_dict[prefix].append(prefixes[n+1][self.prefix_length - 1])
            else:
              phrase_dict[prefix] = [prefixes[n+1][self.prefix_length - 1]] 
        return phrase_dict

    def shred(self, duration):
        prefixes = self.make_prefixes()
        note_dict = self.make_dict()
        sweet_licks = random.choice(prefixes)
        for n in range(self.prefix_length, duration):
            prefix = tuple(sweet_licks[n-self.prefix_length: n])
            suffix = random.choice(note_dict[prefix])
            sweet_licks.append(suffix)
        return sweet_licks

    def write_licks(self, duration, outfile):
        freq_lu = self.freq_dict
        freqs = self.shred(duration)
        data = [] 
        used_freqs = []
        for freq in freqs: 
            used_freqs.append(freq)
            idx = used_freqs.count(freq)-1
            idx = idx % len(freq_lu[freq])
            if len(freq_lu[freq][idx]) > 1024:
                data.append(freq_lu[freq][idx])            
        data = np.concatenate(data)
        flname = './wavs/output/' + outfile
        wavfile.write(flname, rt, data)

        
