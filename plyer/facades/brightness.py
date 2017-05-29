class Brightness(object):
	'''
	Brightness facade.
	'''

	def set(self, level):
		return self._set(level)

	#private

	def _set(self, level):
		raise NotImplementedError()
