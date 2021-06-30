.. Plyer documentation master file, created by
   sphinx-quickstart on Wed Jul  3 15:18:02 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Plyer
================

Plyer is a Python library for accessing features of your hardware / platforms.

Each feature is defined by a facade, and provided by platform specific
implementations, they are used by importing them directly from the `plyer`
package.

For example, to get an implementation of the `gps` facade, and start it you can do:

```python
from plyer import gps

gps.start()
```

Please consult the :mod:`plyer.facades` documentation for the available methods.

.. note::

    Android manage permissions at runtime, and in granular way. Each feature
    can require one or multiple permissions. Plyer will try to ask for the
    necessary permissions the moment they are needed, but they still need to be
    declared at compile time through python-for-android command line, or in
    buildozer.spec.

    Also, there are implications to requesting a permission, as it will briefly
    pause your application. For this reason, it's advised to avoid:
    - starting a plyer feature that require permissions before the app is done
      starting
    - calling multiple features that require different permissions in the same
      frame, unless you previously requested all the necessary permissions.

    If needed, you can normally import the `android` module to manually request
    permissions. Make sure this import is only done when running on Android.

.. automodule:: plyer
    :members:

.. automodule:: plyer.facades
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

