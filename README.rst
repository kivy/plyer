Plyer
====

Plyer is a platform-independant api to use features commonly found on various
platforms, notably mobile ones, in python.

How
---

Plyer tries not to reinvent the wheel, and will call for external libraries to
implement the api in the easiest way, depending on the current platform.

- on python-for-android, pyjnius is used
- on kivy-ios, pyobjius is used
- on windows/mac/linux, commonly found libraries and programs will be used

Support
-------

================================== ============= ============= === ======= === =====
Platform                           Android < 4.0 Android > 4.0 iOS Windows OSX Linux
================================== ============= ============= === ======= === =====
Accelerometer                      X             X
Camera (taking picture)            X             X
GPS                                X             X
Notifications                      X             X                 X       X   X
Text to speech                     X             X                 X       X   X
================================== ============= ============= === ======= === =====
