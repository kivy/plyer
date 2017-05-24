class StoragePath(object):
	'''
	StoragePath facade.
	'''

	def get_home_dir(self):
		return self._get_home_dir()

	def get_external_storage_dir(self):
		return self._get_external_storage_dir()

	def get_root_dir(self):
		return self._get_root_dir()

	def get_documents_dir(self):
		return self._get_documents_dir()

	def get_downloads_dir(self):
		return self._get_downloads_dir()

	def get_movies_dir(self):
		return self._get_movies_dir()

	def get_music_dir(self):
		return self._get_music_dir()

	def get_pictures_dir(self):
		return self._get_pictures_dir()

	def get_application_dir(self):
		return self._get_application_dir()

	#private

	def _get_home_dir(self):
		return NotImplementedError()

	def _get_external_storage_dir(self):
		return NotImplementedError()

	def _get_root_dir(self):
		return NotImplementedError()

	def _get_documents_dir(self):
		return NotImplementedError()

	def _get_downloads_dir(self):
		return NotImplementedError()

	def _get_movies_dir(self):
		return NotImplementedError()

	def _get_music_dir(self):
		return NotImplementedError()

	def _get_pictures_dir(self):
		return NotImplementedError()

	def _get_application_dir(self):
		return NotImplementedError()
