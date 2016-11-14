class Dirs(object):
    '''Dirs Manager facade.

    .. versionadded:: 1.2.5

    On mobile platforms different patterns for storage pathes exist.
    Some location allow stored files to be visible to user, automatically
    synced to cloud storage, or editable by other apps, while other could be
    write-restricted or automatically cleaned.
    Thise module tries to provide proper storage locations for different
    purposes like storing caches, files private for app, configuration files
    and user media files for mobile platforms.
    On desktop it falls back to appdirs functionality.
    '''

    def get_private(self, appname, version=None):
        """ get private storage path

        - appname: required for some platforms to make app-named subdir
        while other (like Android) will point to app-specific directory
        automatically, and parameter will be ignored
        """
        return self._get_private(appname, version)

    def get_cache(self, appname, version=None):
        """ get large cache dir
            On Android it uses getExternalCacheDir() and meant for storing over
            than 1MB. For more reliable location suit for smaller files use
            get_internal_cache() instead, specific to Android.

        - appname: required for some platforms to make app-named subdir
        while other (like Android) will point to app-specific directory
        automatically, and parameter will be ignored
        """
        return self._get_cache(appname, version)

    def get_internal_cache(self, appname, version=None):
        """ get internal cache dir for small files on Android.
            Equals get_cache() on other platforms
        """
        return self._get_internal_cache(appname, version)

    # private

    def _get_private(self, appname=None, version=None):
        raise NotImplementedError()

    def _get_cache(self, appname=None, version=None):
        raise NotImplementedError()

    def _get_internal_cache(self, appname=None, version=None):
        raise NotImplementedError()
