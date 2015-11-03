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

Support
-------

================================== ======= === ======= ==== =====
Platform                           Android iOS Windows OS X Linux
================================== ======= === ======= ==== =====
Accelerometer                      X       X           X    X
Camera (taking picture)            X
GPS                                X       X
Notifications                      X           X       X    X
Text to speech                     X       X   X       X    X
Email (open mail client)           X       X   X       X    X
Vibrator                           X       X
Sms (send messages)                X
Compass                            X       X
Unique ID                          X       X   X       X    X
Gyroscope                          X       X
Battery                            X       X   X       X    X
Native file chooser                            X       X    X
Orientation                        X
Audio recording                    X
Flash                              X       X
================================== ======= === ======= ==== =====
