# Plyer

Plyer is a platform-independent api to use features commonly found on various
platforms, notably mobile ones, in Python.

[![coverage](https://coveralls.io/repos/kivy/plyer/badge.svg?branch=master)](https://coveralls.io/r/kivy/plyer?branch=master)
[![Backers on Open Collective](https://opencollective.com/kivy/backers/badge.svg)](#backers)
[![Sponsors on Open Collective](https://opencollective.com/kivy/sponsors/badge.svg)](#sponsors)
![Continuous Integration with Ubuntu](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20Ubuntu/badge.svg)
![Continuous Integration with OSX](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20OSX/badge.svg)
![Continuous Integration with Windows](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20Windows/badge.svg)
![Deploy to PyPI](https://github.com/kivy/plyer/workflows/Deploy%20to%20PyPI/badge.svg)


## How plyer works?

Plyer tries not to reinvent the wheel, and will call for external libraries to
implement the api in the easiest way, depending on the current platform.

- On Android(python-for-android), pyjnius is used
- On iOS(kivy-ios), pyobjus is used
- On windows/mac/linux, commonly found libraries and programs will be used


## Supported APIs

| Platform                       | Android | iOS | Windows | OS X | Linux |
| ------------------------------ | ------- | --- | ------- | ---- | ----- |
| Accelerometer                  | ✔       | ✔   |         | ✔    | ✔     |
| Audio recording                | ✔       |     | ✔       | ✔    |       |
| Barometer                      | ✔       | ✔   |         |      |       |
| Battery                        | ✔       | ✔   | ✔       | ✔    | ✔     |
| Bluetooth                      | ✔       |     |         | ✔    |       |
| Brightness                     | ✔       | ✔   |         |      | ✔     |
| Call                           | ✔       | ✔   |         |      |       |
| Camera (taking picture)        | ✔       | ✔   |         |      |       |
| Compass                        | ✔       | ✔   |         |      |       |
| CPU count                      |         |     | ✔       | ✔    | ✔     |
| Devicename                     | ✔       |     | ✔       | ✔    | ✔     |
| Email (open mail client)       | ✔       | ✔   | ✔       | ✔    | ✔     |
| Flash                          | ✔       | ✔   |         |      |       |
| GPS                            | ✔       | ✔   |         |      |       |
| Gravity                        | ✔       | ✔   |         |      |       |
| Gyroscope                      | ✔       | ✔   |         |      |       |
| Humidity                       | ✔       |     |         |      |       |
| IR Blaster                     | ✔       |     |         |      |       |
| Keystore                       | ✔       | ✔   | ✔       | ✔    | ✔     |
| Light                          | ✔       |     |         |      |       |
| Native file chooser            | ✔       | ✔   | ✔       | ✔    | ✔     |
| Notifications                  | ✔       |     | ✔       | ✔    | ✔     |
| Orientation                    | ✔       |     |         |      | ✔     |
| Proximity                      | ✔       |     |         |      |       |
| Screenshot                     |         |     | ✔       | ✔    | ✔     |
| SMS (send messages)            | ✔       | ✔   |         |      |       |
| Spatial Orientation            | ✔       | ✔   |         |      |       |
| Speech to text                 | ✔       |     |         |      |       |
| Storage Path                   | ✔       | ✔   | ✔       | ✔    | ✔     |
| Temperature                    | ✔       |     |         |      |       |
| Text to speech                 | ✔       | ✔   | ✔       | ✔    | ✔     |
| Unique ID                      | ✔       | ✔   | ✔       | ✔    | ✔     |
| Vibrator                       | ✔       | ✔   |         |      |       |
| Wifi                           |         |     | ✔       | ✔    | ✔     |


## Installation

To use on desktop: `pip install plyer`
To use in python-for-android/kivy-ios: add `plyer` to your requirements if needed.

## Support

If you need assistance, you can ask for help on our mailing list:

* User Group : https://groups.google.com/group/kivy-users
* Email      : kivy-users@googlegroups.com

Discord channel:

* Server     : https://chat.kivy.org
* Channel    : #dev


## Contributing

We love pull requests and discussing novel ideas. Check out our
[contribution guide](http://kivy.org/docs/contribute.html) and
feel free to improve Plyer.

The following mailing list and IRC channel are used exclusively for
discussions about developing the Kivy framework and its sister projects:

* Dev Group : https://groups.google.com/group/kivy-dev
* Email     : kivy-dev@googlegroups.com

IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy-dev


## License

Plyer is released under the terms of the MIT License. Please refer to the
LICENSE file.

## Contributors

This project exists thanks to all the people who contribute. [[Contribute](http://kivy.org/docs/contribute.html)].

<a href="https://github.com/kivy/plyer/graphs/contributors"><img src="https://contrib.rocks/image?repo=kivy/plyer"/></a>

## Backers

Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/kivy#backer)]

<a href="https://opencollective.com/kivy#backers" target="_blank"><img src="https://opencollective.com/kivy/backers.svg?width=890"></a>


## Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/kivy#sponsor)]

<a href="https://opencollective.com/kivy/sponsor/0/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/1/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/2/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/3/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/4/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/5/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/6/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/7/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/8/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/9/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/9/avatar.svg"></a>
