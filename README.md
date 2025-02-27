# Plyer

Plyer is a platform-independent Python API for accessing hardware features
of various platforms (Android, iOS, macOS, Linux and Windows).

Plyer is managed by the [Kivy Team](https://kivy.org/about.html). It is suitable for
use with Kivy apps, but can be used independently.

[![Backers on Open Collective](https://opencollective.com/kivy/backers/badge.svg)](#backers)
[![Sponsors on Open Collective](https://opencollective.com/kivy/sponsors/badge.svg)](#sponsors)
[![GitHub contributors](https://img.shields.io/github/contributors-anon/kivy/plyer)](https://github.com/kivy/plyer/graphs/contributors)
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
- On iOS ([kivy-ios](https://pypi.org/project/kivy-ios/)) and macOS,
  [pyobjus](https://pypi.org/project/pyobjus/) is used. 
- On Windows, macOS and Linux, other commonly found libraries and programs 
  are used.


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
| Voip                           | ✔       |  ✔  |         |       |       |
| Wifi                           |         |     |    ✔    | ✔     |   ✔   |

## Documentation

Full documentation, including details about the API, is available 
[online](https://plyer.readthedocs.io/en/latest/). If you are not using the
latest version of Plyer, earlier versions of the documentations are linked
from there.

## Installation

To use on desktop: `pip install plyer`
To use in python-for-android and Kivy for iOS, add `plyer` to your requirements
if needed.

## License

Plyer is [MIT licensed](LICENSE), actively developed by a great
community and is supported by many projects managed by the 
[Kivy Organization](https://www.kivy.org/about.html).

## Support

Are you having trouble using Plyer or any of its related projects in the Kivy
ecosystem?
Is there an error you don’t understand? Are you trying to figure out how to use 
it? We have volunteers who can help!

The best channels to contact us for support are listed in the latest 
[Contact Us](https://github.com/kivy/plyer/blob/master/CONTACT.md) document.

## Contributing

Plyer is part of the [Kivy](https://kivy.org) ecosystem - a large group of
products used by many thousands of developers for free, but it
is built entirely by the contributions of volunteers. We welcome (and rely on) 
users who want to give back to the community by contributing to the project.

Contributions can come in many forms. See the latest 
[Contribution Guidelines](https://github.com/kivy/plyer/blob/master/CONTRIBUTING.md)
for how you can help us.

## Code of Conduct

In the interest of fostering an open and welcoming community, we as 
contributors and maintainers need to ensure participation in our project and 
our sister projects is a harassment-free and positive experience for everyone. 
It is vital that all interaction is conducted in a manner conveying respect, 
open-mindedness and gratitude.

Please consult the [latest Code of Conduct](https://github.com/kivy/plyer/blob/master/CODE_OF_CONDUCT.md).

## Contributors

This project exists thanks to 
[all the people who contribute](https://github.com/kivy/plyer/graphs/contributors).
[[Become a contributor](CONTRIBUTING.md)].

<img src="https://contrib.nn.ci/api?repo=kivy/plyer&pages=5&no_bot=true&radius=22&cols=18">

## Backers

Thank you to [all of our backers](https://opencollective.com/kivy)! 
🙏 [[Become a backer](https://opencollective.com/kivy#backer)]

<img src="https://opencollective.com/kivy/backers.svg?width=890&avatarHeight=44&button=false">

## Sponsors

Special thanks to 
[all of our sponsors, past and present](https://opencollective.com/kivy).
Support this project by 
[[becoming a sponsor](https://opencollective.com/kivy#sponsor)].

Here are our top current sponsors. Please click through to see their websites,
and support them as they support us. 

<!--- See https://github.com/orgs/kivy/discussions/15 for explanation of this code. -->
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
<a href="https://opencollective.com/kivy/sponsor/10/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/10/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/11/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/11/avatar.svg"></a>

<a href="https://opencollective.com/kivy/sponsor/12/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/12/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/13/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/13/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/14/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/14/avatar.svg"></a>
<a href="https://opencollective.com/kivy/sponsor/15/website" target="_blank"><img src="https://opencollective.com/kivy/sponsor/15/avatar.svg"></a>
