Changelog
=========

%%version%% (unreleased)
------------------------

- Setup.py: add changelog into the description + fix rst issue. [Mathieu
  Virbel]

- Bump to 1.2.3-dev. [Mathieu Virbel]

1.2.2 (2015-01-27)
------------------

- Bump to 1.2.2. [Mathieu Virbel]

- Update the version to the next dev (missing from the last release)
  [Mathieu Virbel]

- Merge branch 'master' of ssh://github.com/kivy/plyer. [Mathieu Virbel]

- Add initial changelog. [Mathieu Virbel]

- Plyer: fix androidd notification. Closes #93 (credits to @kashifpk)
  [Mathieu Virbel]

- Android/notification: implement a switch to allow usage of API < 16.
  [Mathieu Virbel]

1.2.1 (2014-08-19)
------------------

- Merge pull request #92 from dessant/patch-2. [trivedigaurav]

  fix print statement

- SMS Manager is supported since Android 1.6. [trivedigaurav]

- Merge pull request #90 from trivedigaurav/ios_uuid. [trivedigaurav]

  iOS UUID facade

- Merge pull request #86 from trivedigaurav/ios_battery. [trivedigaurav]

  iOS Battery

- Update compass.py. [trivedigaurav]

- Update gyroscope.py. [trivedigaurav]

- Fix typo. [trivedigaurav]

- Fix typo. [trivedigaurav]

- Fix style. [gtrivedi]

- Merge branch 'trivedigaurav-ios_tts' [gtrivedi]

- Merge pull request #88 from trivedigaurav/ios_email. [trivedigaurav]

  iOS Email Facade

- Merge pull request #89 from trivedigaurav/fix_make. [trivedigaurav]

  Removing build_ext from plyer

- Update accelerometer.py. [trivedigaurav]

- Python 3 compat. [trivedigaurav]

- Python 3 compat. [trivedigaurav]

- Python 3 compat. [trivedigaurav]

- Merge pull request #82 from trivedigaurav/sensors_start_none.
  [trivedigaurav]

  Fix Android enable and disable. Return (None, None, None) until sensor
  data is available

- Merge pull request #68 from trivedigaurav/linux_accel. [trivedigaurav]

  Linux accelerometer facade

- Fix style error. [trivedigaurav]

- Merge pull request #85 from trivedigaurav/battery_ischarging.
  [trivedigaurav]

  Change connected to isCharging

- Merge pull request #80 from ChrisCole42/patch-2. [trivedigaurav]

  Update compass.py

- Merge pull request #79 from trivedigaurav/where_is. [trivedigaurav]

  Use whereis_exe to check for binaries

- Merge pull request #77 from ChrisCole42/patch-1. [trivedigaurav]

  Update compass.py

- Merge pull request #75 from trivedigaurav/maintenance. [trivedigaurav]

  Maintenance merge

- Changed battery Xs to correct columns (ios -> win) [Alexander Taylor]

- Really did fix battery formatting in readme. [Alexander Taylor]

- Fixed battery formatting in readme. [Alexander Taylor]

- Merge pull request #74 from dessant/patch-1. [Akshay Arora]

  facade docstring revision

- Merge pull request #73 from trivedigaurav/battery_info. [Akshay Arora]

  Query Battery info/status

- Merge pull request #71 from trivedigaurav/master. [trivedigaurav]

  Revert "Activity was imported twice"

- Activity was imported twice. [trivedigaurav]

- Merge pull request #70 from trivedigaurav/master. [trivedigaurav]

  Fix tabbing

- Merge pull request #69 from trivedigaurav/gyroscope_fix.
  [trivedigaurav]

  Gyroscope facade proxy declarations

- Merge pull request #67 from trivedigaurav/patch-1. [Akshay Arora]

  Update README.rst

- Typo. [Mathieu Virbel]

- Ios: gyroscope is also supported now. [Mathieu Virbel]

1.2.0 (2014-06-24)
------------------

- Bump to 1.2.0, and mark new classes to 1.2.0. [Mathieu Virbel]

- Merge master. [Mathieu Virbel]

- Merge branch 'master' of ssh://github.com/kivy/plyer. [Mathieu Virbel]

- Merge master. [Mathieu Virbel]

- Merge branch 'master' of ssh://github.com/kivy/plyer. [Mathieu Virbel]

- Merge master. [Mathieu Virbel]

- Merge master. [Mathieu Virbel]

- Merge pull request #52 from mihaineacsu/sms. [Mathieu Virbel]

  Added sms facade, example and android implementation

- Merge pull request #55 from trivedigaurav/osx_accel. [Mathieu Virbel]

  Using sudden motion sensor as accelerometer on OSX

- Merge pull request #62 from trivedigaurav/patch-2. [Mathieu Virbel]

  Update README

- Merge pull request #56 from trivedigaurav/patch-1. [Akshay Arora]

  Update README

- Remove buildozer db. [Mathieu Virbel]

- Merge pull request #46 from matham/master. [akshayaurora]

  Add compat module, remove decoding of strings in notification

- Removed unused import. [Ben Rousch]

- Merge pull request #6 from inclement/vibrate. [Alexander Taylor]

  Added Vibrator facade and android implementation

- Merge pull request #18 from matham/ctypes-notify-window. [Ben Rousch]

  Changes notify to use ctypes instead of win32gui so we could use
  unicode.

- Merge pull request #39 from trivedigaurav/accelerometer_example. [Ben
  Rousch]

  Created an accelerometer example. Uses garden graph to plot the values

- Added examples README. [Ben Rousch]

- Merge pull request #38 from trivedigaurav/tts_example. [Ben Rousch]

  Shows an error popup if there is no TTS

- Merge pull request #37 from trivedigaurav/tts_example. [akshayaurora]

  Text to Speech Example

- Merge pull request #11 from kivy/notification_windows_icon.
  [akshayaurora]

  User-specified icon support for Windows notifications

- Merge pull request #15 from voen/patch-1. [Ben Rousch]

  readme typo corrected

- Merge pull request #10 from kivy/dbus_notify. [akshayaurora]

  Introduce dbus notification

- Fix plyer android.activity import. [Mathieu Virbel]

- Fixed whereis_exe for windows. Fixed espeak TTS for windows. [Ben
  Rousch]

- Merge pull request #5 from inclement/sendemail. [Mathieu Virbel]

  Added an email facade and basic android implementation

- Add missing super() constructor in IosAccelerometer. [Mathieu Virbel]

- Ios: add support for accelerometer on iOS (and motivate brousch again)
  [Mathieu Virbel]

- Add MANIFEST to include LICENSE and README. bump to 1.1.2. [Mathieu
  Virbel]

- Bump to 1.1.1. [Mathieu Virbel]

- Fix setup for pip. [Mathieu Virbel]

- Update readme. [Mathieu Virbel]

- Setup.py: fix readme. [Mathieu Virbel]

- Update readme. [Mathieu Virbel]

- Gps: add versionadded. [Mathieu Virbel]

- Fix documentation version. [Mathieu Virbel]

- Gps: update documentation. [Mathieu Virbel]

- Update setup.py to correctly include win. [Mathieu Virbel]

- Merge branch 'master' of ssh://github.com/kivy/plyer. [Mathieu Virbel]

- Add GPS/android support for plyer. [Mathieu Virbel]

- Add setup.py. [Mathieu Virbel]

- Plyer is now under MIT license. [Mathieu Virbel]

- Fixed incorrect Android tTS return type. [Ben Rousch]

- Merge pull request #1 from kivy/tts. [Ben Rousch]

  TTS!

- Ensure the documentation will find plyer. [Mathieu Virbel]

- Rework how implementation works, and start documentation. [Mathieu
  Virbel]

- First version of plyer, including accelerometer (android), camera
  (android) and notification (android, osx). api is not stabilized.
  [Mathieu Virbel]

- Merge branch 'master' of github.com:kivy/plyer. [tshirtman]

  Conflicts:         readme.md

- Rename to plyer, and uses plateform() from kivy utils. [tshirtman]

- Add android/desktop/ios modules, and auto import from them.
  [tshirtman]

- Initial commit, created simple readme. [tshirtman]


