
import numpy as np 
from note_audio import * 
from audio import * 
import random

class SoloBot(object):
	def __init__(self, ngram_size, training_notes):
		self.ngram_size = ngram_size
		self.training_notes = training_notes

	def ngrams(self):
		for n in xrange(len(self.training_notes) - self.ngram_size - 1):
			yield self.training_notes[n: n + self.ngram_size + 1]

	def markov_states(self):
		states = {}
		for ngrams_plus in self.ngrams():

			k = tuple(self._notes(ngrams_plus[0: self.ngram_size]))
			v = ngrams_plus[-1]

			if k not in states:
				states[k] = [v]
			else:
				states[k] += [v]
		return states

	def _wank(self, wank_count, sinewave=False):
		num = random.randint(0, len(self.training_notes) - self.ngram_size)
		wank_seed = self.training_notes[num: num + self.ngram_size]
		licks = [wank_seed]
		for _ in xrange(wank_count):
			k = tuple(self._notes(licks[-1 * self.ngram_size: ]))
			new_note = random.choice(self.markov_states()[k])
			licks.append(new_note)
		return licks

	def shred(self, num_notes, sinewave=False):
		licks = self._wank(wank_count=num_notes, sinewave=sinewave)
		audio_data = np.array(0, dtype='int16')
		for lick in licks:
			audio_data = np.append(audio_data, lick.dump_audio(sinewave))
		return audio_data

	def _notes(self, note_audio_list):
		return map(lambda n: n.note, note_audio_list)

if __name__ == '__main__':
 
	f = './wavs/input/scales_stuff.wav'
	a = AudioSample.from_wav(f)
	training = a.left_channel().windows().to_played_notes()
	sb = SoloBot(4, training)
	sb.shred(10)





