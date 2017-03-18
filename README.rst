Plyer
=====

Plyer is a platform-independent api to use features commonly found on various
platforms, notably mobile ones, in Python.

How
---

Plyer tries not to reinvent the wheel, and will call for external libraries to
implement the api in the easiest way, depending on the current platform.

- on python-for-android, pyjnius is used
- on kivy-ios, pyobjus is used
- on windows/mac/linux, commonly found libraries and programs will be used

Supported APIs
--------------

================================== ======= === ======= ==== =====
Platform                           Android iOS Windows OS X Linux
================================== ======= === ======= ==== =====
Accelerometer                      X       X           X    X
Barometer                          X
Call                               X       X
Camera (taking picture)            X       X
GPS                                X       X
Gravity                            X
IR Blaster                         X
Notifications                      X           X       X    X
Text to speech                     X       X   X       X    X
Email (open mail client)           X       X   X       X    X
Vibrator                           X       X
Sms (send messages)                X       X
Compass                            X       X
Unique ID                          X       X   X       X    X
Gyroscope                          X       X
Light                              X
Battery                            X       X   X       X    X
Native file chooser                            X       X    X
Orientation                        X
Proximity                          X
Audio recording                    X
Flash                              X       X
Wifi                                           X       X    X
Temperature                        X
================================== ======= === ======= ==== =====

Support
-------

If you need assistance, you can ask for help on our mailing list:

* User Group : https://groups.google.com/group/kivy-users
* Email      : kivy-users@googlegroups.com

We also have an IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy

Contributing
------------

We love pull requests and discussing novel ideas. Check out our
`contribution guide <http://kivy.org/docs/contribute.html>`_ and
feel free to improve Plyer.

The following mailing list and IRC channel are used exclusively for
discussions about developing the Kivy framework and its sister projects:

* Dev Group : https://groups.google.com/group/kivy-dev
* Email     : kivy-dev@googlegroups.com

IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy-dev

License
-------

Plyer is released under the terms of the MIT License. Please refer to the
LICENSE file.
