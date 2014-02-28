from jnius import autoclass

QtActivity = autoclass('org.kde.necessitas.origo.QtActivity')
activity = QtActivity.mActivity
