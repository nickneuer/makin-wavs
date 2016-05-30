
import numpy as np


class Note():
	
	def __init__(self, pitch, octave):
		self.pitch = pitch 
		self.octave = octave

	@staticmethod
	def from_degree(degree):
		notes = ['A', 'Bb', 'B', 'C', 'Db', 'D','Eb', 'E', 'F', 'Gb', 'G', 'Ab']
		return Note( notes[degree % 12] , degree // 12 )

	@staticmethod
	def from_frequency(frequency):
		if frequency == 0:
			return Note(None, None)
		else:
			return Note.from_degree(int(round(12 * np.log2(frequency / 440.0))))

	def __repr__(self):
		return 'Note({}, {})'.format(self.pitch, self.octave)

	def __str__(self):
		if self.pitch:
			return '{}_{}'.format(self.pitch, self.octave)
		else:
			return 'none'
			

