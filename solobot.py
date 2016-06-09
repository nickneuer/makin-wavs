
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

			k = tuple(self._frequencies(ngrams_plus[0: self.ngram_size]))
			v = ngrams_plus[-1]

			if k not in states:
				states[k] = [v]
			else:
				states[k] += [v]
		return states

	def _wank(self, wank_count, sinewave=False):
		num = random.randint(0, len(self.training_notes) - self.ngram_size)
		licks = self._seed()
		for _ in xrange(wank_count):
			k = tuple(self._frequencies(licks[-1 * self.ngram_size: ]))
			try:
				new_note = random.choice(self.markov_states()[k])
				licks.append(new_note)
			except KeyError:
				print 'reseeding...'
				licks += self._seed()
		return licks

	def shred(self, num_notes, sinewave=False):
		licks = self._wank(wank_count=num_notes, sinewave=sinewave)
		audio_data = np.array(0, dtype='int16')
		for lick in licks:
			audio_data = np.append(audio_data, lick.dump_audio(sinewave))
		return audio_data

	def clean_training(self, min_samples=1024 * 4 * 2):
		new_training_notes = [self.training_notes[0]]
		for n, audio_note in enumerate(self.training_notes):
			if n == 0:
				pass

			elif len(audio_note.audio) <= min_samples:
				old = new_training_notes[-1]
				new_training_notes[-1] = NoteAudio(old.note, np.append(old.audio, audio_note.audio))

			else: 
				 new_training_notes.append(audio_note)

		return SoloBot(self.ngram_size, new_training_notes)  

	def _seed(self):
		num = random.randint(0, len(self.training_notes) - self.ngram_size)
		return self.training_notes[num: num + self.ngram_size]

	def _frequencies(self, note_audio_list):
		return map(lambda n: n.note.to_frequency(), note_audio_list)

if __name__ == '__main__':
 	from freq_writer import check_audio
 	import sys

	f = sys.argv[1]
	a = AudioSample.from_wav(f)
	training = a.left_channel().windows().to_training_notes()
	sb = SoloBot(2, training)
	






