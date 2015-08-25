from freq_writer import * 
import sys
from scipy.io import wavfile
import random 
 
# TO DO: get rid of dependency on windows
# Then one MarkovDict can be created and used for multiple files 

class MarkovDict(object):
    def __init__(self, prefix_length, window_size=1024):
        # self.windows = windows
        self.prefix_length = prefix_length
        #self.rate = rate
        self.window_size = window_size
        
    def freq_dict(self, fl): 
        rt, data = wavfile.read(fl)
        windows = make_windows(fl, self.window_size)
        return freq_dict(windows, rt)

    def list_freqs(self, fl):
        rt, windows = rate_and_windows(fl, self.window_size)
        freq_list = get_freqs(windows, rt)
        freq_zip = zip(freq_list, freq_list)
        
        grps = np.array(group_by_threshold(freq_zip, 5))
        grps = map(lambda x: x.T[0], grps)
        grps = map(list, grps)

        freqs = map(lambda grp: stats.mode(grp)[0][0], grps)
        return freqs

    def make_prefixes(self, fl):
        freq_list = self.list_freqs(fl)
        return map(lambda n: freq_list[n-self.prefix_length: n], range(self.prefix_length,len(freq_list)+1))
        
    def make_dict(self, fl):
        prefixes = self.make_prefixes(fl)     
        phrase_dict = dict() 
        for n, prefix in enumerate(prefixes):
          prefix = tuple(prefix)
          if n < len(prefixes)-1:
            if prefix in phrase_dict: 
              phrase_dict[prefix].append(prefixes[n+1][self.prefix_length - 1])
            else:
              phrase_dict[prefix] = [prefixes[n+1][self.prefix_length - 1]] 
        return phrase_dict

    def shred(self, duration, fl):
        prefixes = self.make_prefixes(fl)
        note_dict = self.make_dict(fl)
        sweet_licks = random.choice(prefixes)
        for n in range(self.prefix_length, duration):
            prefix = tuple(sweet_licks[-1 * self.prefix_length:])
            # print "Starting prefix: {0}".format(prefix)
            try:
                suffix = [random.choice(note_dict[prefix])]
                # print "Prefix: {0} \n Suffix: {1}".format(prefix, suffix)
            except KeyError:
                print "invalid key: {0}".format(prefix)
                print "WARN: generating new random seed phrase"
                suffix = random.choice(prefixes)
                print "new_seed = {0}".format(suffix)

            sweet_licks = sweet_licks + suffix
        return sweet_licks

    def write_licks(self, fl, duration, outfile):
        rt, windows = rate_and_windows(fl, self.window_size)
        
        freq_lu = self.freq_dict(fl)
        freqs = self.shred(duration, fl)
        data = [] 
        used_freqs = []
        for freq in freqs: 
            # used_freqs.append(freq)
            # idx = used_freqs.count(freq)-1
            # idx = idx % len(freq_lu[freq])
            freq_data = random.choice(freq_lu[freq])
            if len(freq_data) > 1024:
                data.append(freq_data)            
        data = np.concatenate(data)
        flname = './wavs/output/' + outfile
        wavfile.write(flname, rt, data)

        
