# Plyer

Plyer is a platform-independent Python API for accessing features
of various hardware platforms, especially Android and iOS devices.

Plyer is managed by the [Kivy Team](https://kivy.org/about.html) and is suitable for
use with Kivy apps.

[![Backers on Open Collective](https://opencollective.com/kivy/backers/badge.svg)](https://opencollective.com/kivy)
[![Sponsors on Open Collective](https://opencollective.com/kivy/sponsors/badge.svg)](https://opencollective.com/kivy)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

![PyPI - Version](https://img.shields.io/pypi/v/plyer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/plyer)


[![coverage](https://coveralls.io/repos/kivy/plyer/badge.svg?branch=master)](https://coveralls.io/r/kivy/plyer?branch=master)
![Continuous Integration with Ubuntu](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20Ubuntu/badge.svg) 
![Continuous Integration with OSX](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20OSX/badge.svg)
![Continuous Integration with Windows](https://github.com/kivy/plyer/workflows/Continuous%20Integration%20with%20Windows/badge.svg)
![Deploy to PyPI](https://github.com/kivy/plyer/workflows/Deploy%20to%20PyPI/badge.svg)

## How plyer works?

Plyer tries not to reinvent the wheel, and will call external libraries to
implement the API in the easiest way, depending on the current platform.

- On Android ([python-for-android](https://python-for-android.readthedocs.io/)), [PyJNIus](https://pypi.org/project/pyjnius/) is used.
- On iOS ([kivy-ios](https://pypi.org/project/kivy-ios/)), [pyobjus](https://pypi.org/project/pyobjus/) is used.
- On Windows, macOS and Linux, commonly found libraries and programs will be
used.


## Supported APIs

| Platform                       | Android | iOS | Windows | macOS | Linux |
| ------------------------------ |:-------:|:---:|:-------:|:-----:|:-----:|
| Accelerometer                  | ✔       |  ✔ |         | ✔     |   ✔   |
| Audio recording                | ✔       |     |    ✔    | ✔     |       |
| Barometer                      | ✔       |  ✔  |         |       |       |
| Battery                        | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Bluetooth                      | ✔       |     |         | ✔     |       |
| Brightness                     | ✔       |  ✔  |         |       |   ✔   |
| Call                           | ✔       |  ✔  |         |       |       |
| Camera (taking picture)        | ✔       |  ✔  |         |       |       |
| Compass                        | ✔       |  ✔  |         |       |       |
| CPU count                      |         |     |    ✔    | ✔     |   ✔   |
| Devicename                     | ✔       |     |    ✔    | ✔     |   ✔   |
| Email (open mail client)       | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Flash                          | ✔       |  ✔  |         |       |       |
| GPS                            | ✔       |  ✔  |         |       |       |
| Gravity                        | ✔       |  ✔  |         |       |       |
| Gyroscope                      | ✔       |  ✔  |         |       |       |
| Humidity                       | ✔       |     |         |       |       |
| IR Blaster                     | ✔       |     |         |       |       |
| Keystore                       | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Light                          | ✔       |     |         |       |       |
| Maps                           |         |  ✔  |         | ✔     |       |
| Native file chooser            | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Notifications                  | ✔       |     |    ✔    | ✔     |   ✔   |
| Orientation                    | ✔       |     |         |       |   ✔   |
| Proximity                      | ✔       |     |         |       |       |
| Screenshot                     |         |     |    ✔    | ✔     |   ✔   |
| SMS (send messages)            | ✔       |  ✔  |         | ✔     |       |
| Spatial Orientation            | ✔       |  ✔  |         |       |       |
| Speech to text                 | ✔       |     |         |       |       |
| Storage Path                   | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Temperature                    | ✔       |     |         |       |       |
| Text to speech                 | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Unique ID                      | ✔       |  ✔  |    ✔    | ✔     |   ✔   |
| Vibrator                       | ✔       |  ✔  |         |       |       |
| Wifi                           |         |     |    ✔    | ✔     |   ✔   |


## Installation

To use on desktop: `pip install plyer`
To use in python-for-android/kivy-ios: add `plyer` to your requirements if needed.

## License

Kivy for iOS is [MIT licensed](LICENSE), actively developed by a great
community and is supported by many projects managed by the 
[Kivy Organization](https://www.kivy.org/about.html).

## Support

Are you having trouble using the Kivy framework, or any of its related projects?
Is there an error you don’t understand? Are you trying to figure out how to use 
it? We have volunteers who can help!

The best channels to contact us for support are listed in the latest 
[Contact Us](https://github.com/kivy/kivy/blob/master/CONTACT.md) document.

## Contributing

Kivy is a large product used by many thousands of developers for free, but it 
is built entirely by the contributions of volunteers. We welcome (and rely on) 
users who want to give back to the community by contributing to the project.

Contributions can come in many forms. See the latest 
[Kivy Contribution Guidelines](https://github.com/kivy/kivy/blob/master/CONTRIBUTING.md)
for how you can help us.

## Code of Conduct

In the interest of fostering an open and welcoming community, we as 
contributors and maintainers need to ensure participation in our project and 
our sister projects is a harassment-free and positive experience for everyone. 
It is vital that all interaction is conducted in a manner conveying respect, 
open-mindedness and gratitude.

Please consult the [latest Kivy Code of Conduct](https://github.com/kivy/kivy/blob/master/CODE_OF_CONDUCT.md).