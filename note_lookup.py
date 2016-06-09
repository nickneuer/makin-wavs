
import numpy as np


class Note():
	
	notes = ['A', 'Bb', 'B', 'C', 'Db', 'D','Eb', 'E', 'F', 'Gb', 'G', 'Ab']
	# I know, I know. No microtonal support, so pedestrian.

	def __init__(self, pitch, octave):
		self.pitch = pitch 
		self.octave = octave

	@staticmethod
	def from_degree(degree):
		return Note( Note.notes[degree % 12] , degree // 12 )

	@staticmethod
	def from_frequency(frequency):
		if frequency == 0:
			return Note(None, 0)
		else:
			return Note.from_degree(int(round(12 * np.log2(frequency / 440.0))))

	def __repr__(self):
		return "Note('{}', {})".format(self.pitch, self.octave)

	def __str__(self):
		if self.pitch:
			return '{}_{}'.format(self.pitch, self.octave)
		else:
			return 'none'

	def to_degree(self):
		return Note.notes.index(self.pitch) + self.octave * 12

	def to_frequency(self):
		if self.pitch:
			return round(440 * np.power(np.power(2, 1 / 12.), self.to_degree()))
		else:
			return 0

			


