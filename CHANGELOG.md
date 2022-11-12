# Change Log

## [2.1.0](https://github.com/kivy/plyer/tree/2.1.0) (2022-11-12)

[Full Changelog](https://github.com/kivy/plyer/compare/2.0.0...2.1.0)

**Implemented enhancements:**

- Use xdg-desktop-portal for Notification inside Flatpak [\#680](https://github.com/kivy/plyer/pull/680) ([JakobDev](https://github.com/JakobDev))

**Closed issues:**

- Exception is thrown on try to play recorded audio clip [\#713](https://github.com/kivy/plyer/issues/713)
- iOS: filechooser - multiple files selection is not working [\#707](https://github.com/kivy/plyer/issues/707)
- Speech to text is not working with api 30 or more [\#693](https://github.com/kivy/plyer/issues/693)
- Traceback \(most recent call last\):
   File "jnius/jnius\_proxy.pxi", line 50, in jnius.jnius.PythonJavaClass.invoke
   File "jnius/jnius\_proxy.pxi", line 74, in jnius.jnius.PythonJavaClass.\_invoke
 NotImplementedError: The method \('onLocationChanged', \('V', \('Ljava/util/List;',\)\)\) is not implemented [\#687](https://github.com/kivy/plyer/issues/687)
- Notify on Windows but without archiving notifications [\#684](https://github.com/kivy/plyer/issues/684)
- Notification icon as base64 instead of path [\#679](https://github.com/kivy/plyer/issues/679)
- plyer's last release was ~2 years ago, the number of open PRs is absurd, and the last meaningful commit was months ago [\#674](https://github.com/kivy/plyer/issues/674)
- iOS Filechooser that picks all document types \(UIDocumentPickerViewController\) [\#673](https://github.com/kivy/plyer/issues/673)
- Python dbus error on Linux when sending notification [\#658](https://github.com/kivy/plyer/issues/658)
- Is that project dead? [\#650](https://github.com/kivy/plyer/issues/650)
- Notification for android not working \[ Drawable.icon \] [\#647](https://github.com/kivy/plyer/issues/647)
- audio don't work on android [\#644](https://github.com/kivy/plyer/issues/644)
- Unittests are failing on new clone [\#637](https://github.com/kivy/plyer/issues/637)
- Proposing a PR to fix a few small typos [\#622](https://github.com/kivy/plyer/issues/622)
- Remove python2 mentions from setup.py [\#608](https://github.com/kivy/plyer/issues/608)
- vibrator on android 10 java.lang.SecurityException [\#606](https://github.com/kivy/plyer/issues/606)
- How to change prompt input to upper or lower case in JS? [\#603](https://github.com/kivy/plyer/issues/603)
- Does this repo is maintained? [\#592](https://github.com/kivy/plyer/issues/592)
- Plyer notification not working on android [\#591](https://github.com/kivy/plyer/issues/591)
- Feature Request: Add Intent to Android Gallery\(for Pictures\) [\#588](https://github.com/kivy/plyer/issues/588)
- plyer.filechooser.save\_file doesn't work on macOS X Catalina [\#578](https://github.com/kivy/plyer/issues/578)
- macOS notification NSUserNotificationCenter is deprecated + missing Info.plist [\#449](https://github.com/kivy/plyer/issues/449)

**Merged pull requests:**

- action-gh-release now uses `github.token` [\#724](https://github.com/kivy/plyer/pull/724) ([misl6](https://github.com/misl6))
- Bump version to 2.1.0 for release [\#723](https://github.com/kivy/plyer/pull/723) ([misl6](https://github.com/misl6))
- Bump action-gh-release to a newer version [\#721](https://github.com/kivy/plyer/pull/721) ([misl6](https://github.com/misl6))
- Update supported Python versions [\#720](https://github.com/kivy/plyer/pull/720) ([misl6](https://github.com/misl6))
- Fixes some E275. + other minor PEP8 fixes [\#711](https://github.com/kivy/plyer/pull/711) ([misl6](https://github.com/misl6))
- Document linux support for orientation [\#709](https://github.com/kivy/plyer/pull/709) ([rshah713](https://github.com/rshah713))
- Document supported platforms for humidity [\#704](https://github.com/kivy/plyer/pull/704) ([rshah713](https://github.com/rshah713))
- Keyword should only hold name of license [\#701](https://github.com/kivy/plyer/pull/701) ([rshah713](https://github.com/rshah713))
- Document supported platforms in native filechooser [\#700](https://github.com/kivy/plyer/pull/700) ([rshah713](https://github.com/rshah713))
- Fix Keystore comment to point at correct class [\#697](https://github.com/kivy/plyer/pull/697) ([rshah713](https://github.com/rshah713))
- Add missing platform for barometer [\#695](https://github.com/kivy/plyer/pull/695) ([rshah713](https://github.com/rshah713))
- Add missing platforms in audio [\#694](https://github.com/kivy/plyer/pull/694) ([rshah713](https://github.com/rshah713))
- Fixes a failing test for notification [\#692](https://github.com/kivy/plyer/pull/692) ([misl6](https://github.com/misl6))
- Fixes style check [\#691](https://github.com/kivy/plyer/pull/691) ([misl6](https://github.com/misl6))
- Clear documentation for Processors [\#689](https://github.com/kivy/plyer/pull/689) ([rshah713](https://github.com/rshah713))
- Create clear documentation for Keystore [\#688](https://github.com/kivy/plyer/pull/688) ([rshah713](https://github.com/rshah713))
- Added tick in ios native file chooser row [\#685](https://github.com/kivy/plyer/pull/685) ([Neizvestnyj](https://github.com/Neizvestnyj))
- :zap: Fix pep8 violations [\#678](https://github.com/kivy/plyer/pull/678) ([Zen-CODE](https://github.com/Zen-CODE))
- :hammer: Fix pep 8 failure for CICD [\#677](https://github.com/kivy/plyer/pull/677) ([Zen-CODE](https://github.com/Zen-CODE))
- fix some errors in readme file [\#676](https://github.com/kivy/plyer/pull/676) ([AdamMusa](https://github.com/AdamMusa))
- android 11+ compatibility Documents folder [\#672](https://github.com/kivy/plyer/pull/672) ([moonpyx](https://github.com/moonpyx))
- Use sys.getandroidapilevel for more robust Android detection [\#670](https://github.com/kivy/plyer/pull/670) ([rdb](https://github.com/rdb))
- More robust way to get application icon on Android for notification [\#669](https://github.com/kivy/plyer/pull/669) ([rdb](https://github.com/rdb))
- Added the ability to track the closure of the file manager without selecting content [\#667](https://github.com/kivy/plyer/pull/667) ([Neizvestnyj](https://github.com/Neizvestnyj))
- Fix bug, when user canceled filechooser, `on_selection` does not dispatched [\#666](https://github.com/kivy/plyer/pull/666) ([Neizvestnyj](https://github.com/Neizvestnyj))
- Bigger buffer, allows large selection [\#655](https://github.com/kivy/plyer/pull/655) ([akshayaurora](https://github.com/akshayaurora))
- fix: fix filechooser save dialog for the KDE [\#652](https://github.com/kivy/plyer/pull/652) ([psyrykh](https://github.com/psyrykh))
- Change R$drawable to R$mipmap in notification.py for android platform [\#648](https://github.com/kivy/plyer/pull/648) ([masterjoseph914](https://github.com/masterjoseph914))
- linux/storagepath: fixup a host of issues [\#646](https://github.com/kivy/plyer/pull/646) ([rski](https://github.com/rski))
- Change `PythonActivity` java class [\#642](https://github.com/kivy/plyer/pull/642) ([Neizvestnyj](https://github.com/Neizvestnyj))
- Enabled transient notifications on Linux [\#639](https://github.com/kivy/plyer/pull/639) ([olumidesan](https://github.com/olumidesan))
- updated-device-name-implementation-for-backward-compatibility [\#634](https://github.com/kivy/plyer/pull/634) ([ljnath](https://github.com/ljnath))
- Added contributors in readme.md file [\#633](https://github.com/kivy/plyer/pull/633) ([ljnath](https://github.com/ljnath))
- Fixed pep8 errors [\#632](https://github.com/kivy/plyer/pull/632) ([ljnath](https://github.com/ljnath))
- Removed python2.6|7 reference and added reference for python 3.6|7|8  [\#631](https://github.com/kivy/plyer/pull/631) ([ljnath](https://github.com/ljnath))
- Support to get android device name or hostname for linux and windows [\#630](https://github.com/kivy/plyer/pull/630) ([ljnath](https://github.com/ljnath))
- \#611 add filters for file chooser on android [\#624](https://github.com/kivy/plyer/pull/624) ([akshayaurora](https://github.com/akshayaurora))
- docs: fix a few simple typos [\#623](https://github.com/kivy/plyer/pull/623) ([akshayaurora](https://github.com/akshayaurora))
- Add check for Trinity Desktop Environment [\#620](https://github.com/kivy/plyer/pull/620) ([akshayaurora](https://github.com/akshayaurora))
- FileChooser: MacOS: Use objectAtIndex\_ to get multiple items [\#618](https://github.com/kivy/plyer/pull/618) ([akshayaurora](https://github.com/akshayaurora))
- add installation section in README.md [\#563](https://github.com/kivy/plyer/pull/563) ([tshirtman](https://github.com/tshirtman))

## [2.0.0](https://github.com/kivy/plyer/tree/2.0.0) (2020-11-09)

[Full Changelog](https://github.com/kivy/plyer/compare/1.4.3...2.0.0)

**Closed issues:**

- Macox notification - AttributeError: 'NoneType' object has no attribute 'setDelegate\_' [\#586](https://github.com/kivy/plyer/issues/586)
- Can't display notifications with Plyer [\#582](https://github.com/kivy/plyer/issues/582)
- Unable to set app orientation [\#579](https://github.com/kivy/plyer/issues/579)
- Does plyer allow you to open another app? [\#577](https://github.com/kivy/plyer/issues/577)
- Calling notification.notify\(\) raises "No Usable Implementation Found!" Error on Android [\#575](https://github.com/kivy/plyer/issues/575)
- tts is not working [\#572](https://github.com/kivy/plyer/issues/572)
- bluetooth for Android [\#571](https://github.com/kivy/plyer/issues/571)
- raise NotImplementedError\(\)  NotImplementedError when I use tts  [\#567](https://github.com/kivy/plyer/issues/567)
- Filter variable may be uninitialized in MacOSX filechooser [\#566](https://github.com/kivy/plyer/issues/566)
- Plyer camera cannot save image to the IOS phone [\#561](https://github.com/kivy/plyer/issues/561)
- How to turn on gps  ?? [\#556](https://github.com/kivy/plyer/issues/556)
- How to disable mock location \(fake gps\) in kivy  [\#555](https://github.com/kivy/plyer/issues/555)
- Release notes for v 1.4.3? [\#550](https://github.com/kivy/plyer/issues/550)
- battery.status isCharging always shows false in WINDOWS [\#541](https://github.com/kivy/plyer/issues/541)
- Filechooser on mac: using path, crashes python [\#524](https://github.com/kivy/plyer/issues/524)
- Android Filechooser not working [\#512](https://github.com/kivy/plyer/issues/512)

**Merged pull requests:**

- Some APIs are only available for open panels. [\#590](https://github.com/kivy/plyer/pull/590) ([matham](https://github.com/matham))
- Fix uninitialized variable in MacOSX filechooser. [\#568](https://github.com/kivy/plyer/pull/568) ([Mulugruntz](https://github.com/Mulugruntz))
- Fixing crash on MacOSX filechooser [\#565](https://github.com/kivy/plyer/pull/565) ([Mulugruntz](https://github.com/Mulugruntz))
- Uses Python 3 syntax [\#554](https://github.com/kivy/plyer/pull/554) ([AndreMiras](https://github.com/AndreMiras))
- Feature/drop python2 [\#553](https://github.com/kivy/plyer/pull/553) ([AndreMiras](https://github.com/AndreMiras))
- Fixes linter errors [\#552](https://github.com/kivy/plyer/pull/552) ([AndreMiras](https://github.com/AndreMiras))
- Remove unused linters [\#548](https://github.com/kivy/plyer/pull/548) ([ghost](https://github.com/ghost))
- Fix linter warnings [\#547](https://github.com/kivy/plyer/pull/547) ([ghost](https://github.com/ghost))
- Modification of Status isCharging in windows [\#546](https://github.com/kivy/plyer/pull/546) ([irm19](https://github.com/irm19))

## [1.4.3](https://github.com/kivy/plyer/tree/1.4.3) (2020-03-27)

[Full Changelog](https://github.com/kivy/plyer/compare/1.4.2...1.4.3)

**Closed issues:**

- IOS - GPS : 'IosGPS' object has no attribute '\_location\_manager' [\#538](https://github.com/kivy/plyer/issues/538)
- Android FileChooser crashes when back button pressed [\#534](https://github.com/kivy/plyer/issues/534)
- Notification not working on android [\#533](https://github.com/kivy/plyer/issues/533)
- FileChooser on Android: "on selection" fires multiple times. [\#530](https://github.com/kivy/plyer/issues/530)
- KIVY cannot access the android camera.. [\#521](https://github.com/kivy/plyer/issues/521)
- No notification icons on Linux \(Gnome\) [\#514](https://github.com/kivy/plyer/issues/514)
- Vibrator is not working on Android [\#509](https://github.com/kivy/plyer/issues/509)
- notification.notify crashes Android Pie devices [\#504](https://github.com/kivy/plyer/issues/504)
- Vibrate revision in api 26 [\#501](https://github.com/kivy/plyer/issues/501)

**Merged pull requests:**

- Fix linter warnings in examples/gps/main.py [\#545](https://github.com/kivy/plyer/pull/545) ([ghost](https://github.com/ghost))
- Switch to GitHub actions [\#544](https://github.com/kivy/plyer/pull/544) ([ghost](https://github.com/ghost))
- Fix crash in Android Notification \(SDK\_INT \>= 26\) [\#543](https://github.com/kivy/plyer/pull/543) ([ghost](https://github.com/ghost))
- Add native iOS FileBrowser [\#542](https://github.com/kivy/plyer/pull/542) ([Zen-CODE](https://github.com/Zen-CODE))
- Prevent crash when cancelling filechooser [\#536](https://github.com/kivy/plyer/pull/536) ([Zen-CODE](https://github.com/Zen-CODE))
- Make win filechooser use modern windows browser and fix small issues. [\#535](https://github.com/kivy/plyer/pull/535) ([matham](https://github.com/matham))
- Prevent re-binding of callback on each call [\#532](https://github.com/kivy/plyer/pull/532) ([Zen-CODE](https://github.com/Zen-CODE))
- Add permission request to plyer GPS example [\#529](https://github.com/kivy/plyer/pull/529) ([Zen-CODE](https://github.com/Zen-CODE))
- Handle absence of LinuxFileChooser backend [\#526](https://github.com/kivy/plyer/pull/526) ([Cheaterman](https://github.com/Cheaterman))
- Fix vibrator, which was not working on Android devices. [\#523](https://github.com/kivy/plyer/pull/523) ([ghost](https://github.com/ghost))
- Added logic to support the `on_status` method of the gps facade for i… [\#519](https://github.com/kivy/plyer/pull/519) ([Dirk-Sandberg](https://github.com/Dirk-Sandberg))
- Fix default audio file\_path assignment error, file\_path change for Py3 [\#518](https://github.com/kivy/plyer/pull/518) ([Nephyx](https://github.com/Nephyx))
- Add Windows applications storage path [\#517](https://github.com/kivy/plyer/pull/517) ([magnusvmt](https://github.com/magnusvmt))
- fix typo in supported API list [\#516](https://github.com/kivy/plyer/pull/516) ([holdbar](https://github.com/holdbar))
- fix the issue that tts.speak\(\) crashes on android [\#511](https://github.com/kivy/plyer/pull/511) ([Chao-Jen](https://github.com/Chao-Jen))
- Addresses plyer issue \#240. [\#502](https://github.com/kivy/plyer/pull/502) ([Dirk-Sandberg](https://github.com/Dirk-Sandberg))
- Update README.md to add opencollective [\#499](https://github.com/kivy/plyer/pull/499) ([tito](https://github.com/tito))
- Bump to 1.4.0 for release [\#496](https://github.com/kivy/plyer/pull/496) ([KeyWeeUsr](https://github.com/KeyWeeUsr))

## [1.4.2](https://github.com/kivy/plyer/tree/1.4.2) (2019-09-05)

[Full Changelog](https://github.com/kivy/plyer/compare/1.4.1...1.4.2)

## [1.4.1](https://github.com/kivy/plyer/tree/1.4.1) (2019-09-05)

[Full Changelog](https://github.com/kivy/plyer/compare/1.4.0...1.4.1)

**Closed issues:**

- I'll be Working on Linux audio [\#497](https://github.com/kivy/plyer/issues/497)
- Notification and service [\#494](https://github.com/kivy/plyer/issues/494)
- Windows notification - NotImplementedError: No usable implementation found! [\#485](https://github.com/kivy/plyer/issues/485)
- macOS notification NSUserNotificationCenter is deprecated + missing Info.plist [\#449](https://github.com/kivy/plyer/issues/449)

## [1.4.0](https://github.com/kivy/plyer/tree/1.4.0) (2018-12-31)

[Full Changelog](https://github.com/kivy/plyer/compare/1.3.2...1.4.0)

**Implemented enhancements:**

- Windows microphone support [\#179](https://github.com/kivy/plyer/issues/179)

**Closed issues:**

- jnius.jnius.JavaException: Class not found 'android/content/INTENT' [\#479](https://github.com/kivy/plyer/issues/479)
- macOS storagepath uses non-standard path for get\_home\_dir\(\) [\#450](https://github.com/kivy/plyer/issues/450)
- Example Applications break down on a real device [\#338](https://github.com/kivy/plyer/issues/338)
- Feature request: Accelerometer on Linux \(computers\) [\#9](https://github.com/kivy/plyer/issues/9)
- Linux wifi implementation via rockymeza/wifi is broken [\#487](https://github.com/kivy/plyer/issues/487)
- Hardcoded 'wlan0' does not work on all devices [\#477](https://github.com/kivy/plyer/issues/477)
- GNU/Linux wifi disconnect\(\) not working on Ubuntu 15.04+ [\#452](https://github.com/kivy/plyer/issues/452)
- Plyer Email [\#420](https://github.com/kivy/plyer/issues/420)
- notification not working on android [\#402](https://github.com/kivy/plyer/issues/402)
- plyer.accelerometer not working with Kivy Launcher [\#401](https://github.com/kivy/plyer/issues/401)
- New PyPI release after 1.3.0 [\#400](https://github.com/kivy/plyer/issues/400)
- plyer.notify.notification doesn't show ticker in Android [\#378](https://github.com/kivy/plyer/issues/378)
- plyer.uniqueid.id causes crash on Android with sdl2 [\#245](https://github.com/kivy/plyer/issues/245)
- audio: JVM exception occurred: setAudioSource failed. [\#210](https://github.com/kivy/plyer/issues/210)
- Something wrong with encoding in AndroidNotification [\#175](https://github.com/kivy/plyer/issues/175)

**Merged pull requests:**

- Implement WiFi for Linux with nmcli [\#495](https://github.com/kivy/plyer/pull/495) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Enhance Android notifications with toast and big icons [\#493](https://github.com/kivy/plyer/pull/493) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix android notifications missing channel on Oreo and later [\#492](https://github.com/kivy/plyer/pull/492) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add Android Native filechooser and external SD card path to StoragePath [\#491](https://github.com/kivy/plyer/pull/491) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix OSX builds on Travis [\#490](https://github.com/kivy/plyer/pull/490) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add audio recording and playing for Windows [\#489](https://github.com/kivy/plyer/pull/489) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add support for interfaces in Linux WiFi [\#488](https://github.com/kivy/plyer/pull/488) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- macOS tests - audio, battery, bluetooth, storagepath [\#482](https://github.com/kivy/plyer/pull/482) ([Nephyx](https://github.com/Nephyx))
- Change 'Speech' to 'STT' [\#484](https://github.com/kivy/plyer/pull/484) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- New extended CPU details implementation [\#483](https://github.com/kivy/plyer/pull/483) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix uniqueid for linux platform [\#481](https://github.com/kivy/plyer/pull/481) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix CI jobs reporting wrong coverage \(non-imported modules ignored\) [\#480](https://github.com/kivy/plyer/pull/480) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- thegrymek: Android speech recognition [\#471](https://github.com/kivy/plyer/pull/471) ([KeyWeeUsr](https://github.com/KeyWeeUsr))

## [1.3.2](https://github.com/kivy/plyer/tree/1.3.2) (2018-11-16)

[Full Changelog](https://github.com/kivy/plyer/compare/1.3.1...1.3.2)

**Implemented enhancements:**

- \[Feature Request\] Termux support [\#360](https://github.com/kivy/plyer/issues/360)
- storage path support [\#152](https://github.com/kivy/plyer/issues/152)
- unicode broken in notifications on windows 8. [\#17](https://github.com/kivy/plyer/issues/17)
- Feature Request: Add adjustable tooltip text to Windows notification [\#14](https://github.com/kivy/plyer/issues/14)

**Closed issues:**

- plyer notifications raising NotImplementedError on android [\#467](https://github.com/kivy/plyer/issues/467)
- TypeError when running examples in Python 3 [\#392](https://github.com/kivy/plyer/issues/392)
- when i use buildozer and python3crystax to build apk  it not work ? [\#380](https://github.com/kivy/plyer/issues/380)
- Windows filechooser crash [\#375](https://github.com/kivy/plyer/issues/375)
- Using the camera crashes the app [\#369](https://github.com/kivy/plyer/issues/369)
- after calling an plyer audio function from an accelerometer function, App crashes. [\#361](https://github.com/kivy/plyer/issues/361)
- uniqueid.id fails under android and windows7 32bit python2.7 [\#277](https://github.com/kivy/plyer/issues/277)
- Strange string returned by filechooser on Windows [\#177](https://github.com/kivy/plyer/issues/177)
- Email Support for OSX [\#32](https://github.com/kivy/plyer/issues/32)
- GPS Support for iOS [\#22](https://github.com/kivy/plyer/issues/22)
- Camera Support for iOS [\#21](https://github.com/kivy/plyer/issues/21)
- Example app for Camera facade [\#16](https://github.com/kivy/plyer/issues/16)

**Merged pull requests:**

- Move TODO item to a separate issue [\#478](https://github.com/kivy/plyer/pull/478) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add @deprecated decorator [\#476](https://github.com/kivy/plyer/pull/476) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fixed macOS using non-standard path for get\_home\_dir\(\) [\#475](https://github.com/kivy/plyer/pull/475) ([Nephyx](https://github.com/Nephyx))
- Removed unnecessary grep dependency [\#474](https://github.com/kivy/plyer/pull/474) ([Nephyx](https://github.com/Nephyx))
- Add enable & disable WiFi for Linux and MacOS [\#473](https://github.com/kivy/plyer/pull/473) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Cleaning the plyer root directory and CI scripts [\#468](https://github.com/kivy/plyer/pull/468) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add more distros via Docker images [\#466](https://github.com/kivy/plyer/pull/466) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add Linux Screenshot with X11's X Window Dump [\#463](https://github.com/kivy/plyer/pull/463) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Revert uppercase on autoclass values [\#462](https://github.com/kivy/plyer/pull/462) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fixing Java class name [\#461](https://github.com/kivy/plyer/pull/461) ([clevermindgames](https://github.com/clevermindgames))
- Increase timeout for notification test [\#460](https://github.com/kivy/plyer/pull/460) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add Windows Screenshot with ctypes+pywin32 [\#459](https://github.com/kivy/plyer/pull/459) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add screenshot test for OSX [\#458](https://github.com/kivy/plyer/pull/458) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- OSX Screenshot \(Rebased PR \#324\) [\#457](https://github.com/kivy/plyer/pull/457) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Rebased PR \#239 + fixes [\#455](https://github.com/kivy/plyer/pull/455) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Bump to 1.3.2.dev0 [\#446](https://github.com/kivy/plyer/pull/446) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Bump to 1.3.1 [\#445](https://github.com/kivy/plyer/pull/445) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add extra options for installation via setuptools [\#438](https://github.com/kivy/plyer/pull/438) ([KeyWeeUsr](https://github.com/KeyWeeUsr))

## [1.3.1](https://github.com/kivy/plyer/tree/1.3.1) (2018-10-14)

[Full Changelog](https://github.com/kivy/plyer/compare/1.3.0...1.3.1)

**Implemented enhancements:**

- Audio recording for macOS [\#428](https://github.com/kivy/plyer/pull/428) ([Nephyx](https://github.com/Nephyx))

**Closed issues:**

- plyer.wifi.is\_enabled\(\) always return false running in python3 [\#436](https://github.com/kivy/plyer/issues/436)
- kivy-ios fails to build plyer [\#417](https://github.com/kivy/plyer/issues/417)
- Python 3 TabError [\#398](https://github.com/kivy/plyer/issues/398)
- is there a way of using the front camera instead of back  [\#391](https://github.com/kivy/plyer/issues/391)
- storagepath.py  \_get\_application\_dir: NotImplementedError [\#389](https://github.com/kivy/plyer/issues/389)
- plyer app crashes on android [\#387](https://github.com/kivy/plyer/issues/387)
- Can't pip install plyer through git [\#385](https://github.com/kivy/plyer/issues/385)
- speech to text [\#382](https://github.com/kivy/plyer/issues/382)
- text2speech doesn't work on platform Linux [\#372](https://github.com/kivy/plyer/issues/372)
- Changing file\_path in audio.py example is not working [\#356](https://github.com/kivy/plyer/issues/356)
- How to change file\_path of audio in plyer? [\#355](https://github.com/kivy/plyer/issues/355)
- Accelerometer in plyer [\#354](https://github.com/kivy/plyer/issues/354)
- iOS Gyroscope crashes [\#352](https://github.com/kivy/plyer/issues/352)
- Need keystore for storing user credentials  [\#350](https://github.com/kivy/plyer/issues/350)
- plyer examples app always crashes in android phones, It says "Unfortunately "Name of app" has stopped working." [\#349](https://github.com/kivy/plyer/issues/349)
- Notification not working on Windows [\#333](https://github.com/kivy/plyer/issues/333)
- Accelerometer not working on linux [\#327](https://github.com/kivy/plyer/issues/327)
- 1.3.0 broke notifications on Windows [\#318](https://github.com/kivy/plyer/issues/318)
- No encoding and °C causes SyntaxError [\#312](https://github.com/kivy/plyer/issues/312)
- GPS double output on output return value [\#302](https://github.com/kivy/plyer/issues/302)
- Cannot import wifi module in windows [\#272](https://github.com/kivy/plyer/issues/272)

**Merged pull requests:**

- Add note about Windows icon format [\#444](https://github.com/kivy/plyer/pull/444) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Mark new audio recording feature in README.rst [\#443](https://github.com/kivy/plyer/pull/443) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix not decoding bytes in Linux orientation.py [\#442](https://github.com/kivy/plyer/pull/442) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix b' embedded in the path string for Windows' choose\_dir\(\) [\#441](https://github.com/kivy/plyer/pull/441) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add missing parameter for Windows' WlanCloseHandle\(\) [\#440](https://github.com/kivy/plyer/pull/440) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Revert facades/wifi.py change from PR \#301 [\#439](https://github.com/kivy/plyer/pull/439) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Update wifi.py [\#437](https://github.com/kivy/plyer/pull/437) ([Vibhu-Agarwal](https://github.com/Vibhu-Agarwal))
- Remove notification webhook from travis [\#434](https://github.com/kivy/plyer/pull/434) ([dessant](https://github.com/dessant))
- Fix Travis build for pull requests [\#432](https://github.com/kivy/plyer/pull/432) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Changed OSX storage path from ctypes to pyobjus [\#431](https://github.com/kivy/plyer/pull/431) ([Nephyx](https://github.com/Nephyx))
- Fix Pylint errors W0150, W0511, W0601, W0603, W0610 [\#430](https://github.com/kivy/plyer/pull/430) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix Pylint errors W0611, W0612, W0622, W0702, W0703 [\#427](https://github.com/kivy/plyer/pull/427) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Disable all Pylint errors to fix red jobs [\#426](https://github.com/kivy/plyer/pull/426) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Downgrade Travis due to missing docker service on Ubuntu Bionic [\#425](https://github.com/kivy/plyer/pull/425) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Switch from Ubuntu Trusty to Ubuntu Bionic LTS [\#424](https://github.com/kivy/plyer/pull/424) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix style issues in utils, compat and setup.py [\#423](https://github.com/kivy/plyer/pull/423) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Clickable notifications, fixes \#154 [\#422](https://github.com/kivy/plyer/pull/422) ([AndreMiras](https://github.com/AndreMiras))
- Fix style in test\_facade.py [\#418](https://github.com/kivy/plyer/pull/418) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix pep8 issues in files [\#416](https://github.com/kivy/plyer/pull/416) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add script for CI deployment to PyPI [\#413](https://github.com/kivy/plyer/pull/413) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix travis to use real branch instead of detached HEAD [\#412](https://github.com/kivy/plyer/pull/412) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add linux battery from sysclass [\#411](https://github.com/kivy/plyer/pull/411) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Switch to unicode in macosx battery.py [\#410](https://github.com/kivy/plyer/pull/410) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix test\_facade failing for Py3 by switching to Mocks [\#409](https://github.com/kivy/plyer/pull/409) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Add Dockerfiles for testing, fix tests and style [\#408](https://github.com/kivy/plyer/pull/408) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Implemented storagepath in linux [\#407](https://github.com/kivy/plyer/pull/407) ([Sires0](https://github.com/Sires0))
- Improve messages for missing dependencies [\#406](https://github.com/kivy/plyer/pull/406) ([dolang](https://github.com/dolang))
- Updates README.rst, removes dup in supported API [\#403](https://github.com/kivy/plyer/pull/403) ([AndreMiras](https://github.com/AndreMiras))
- why should decode 'l' again and again [\#396](https://github.com/kivy/plyer/pull/396) ([xhimanshuz](https://github.com/xhimanshuz))
- Correcting issue https://github.com/kivy/plyer/issues/392 for linux p… [\#395](https://github.com/kivy/plyer/pull/395) ([ghost](https://github.com/ghost))
- Number Of Processors for Linux Platform [\#394](https://github.com/kivy/plyer/pull/394) ([salil-gtm](https://github.com/salil-gtm))
- enhancement: bluetooth status [\#388](https://github.com/kivy/plyer/pull/388) ([kapilnayar](https://github.com/kapilnayar))
- Show that bluetooth is not supported [\#379](https://github.com/kivy/plyer/pull/379) ([zerox1212](https://github.com/zerox1212))
- Arrange APIs table in alphabetical order [\#377](https://github.com/kivy/plyer/pull/377) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Add list of supported platforms to facade [\#376](https://github.com/kivy/plyer/pull/376) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Add iOS api for storage path [\#374](https://github.com/kivy/plyer/pull/374) ([sumitmadhwani](https://github.com/sumitmadhwani))
- update readme [\#373](https://github.com/kivy/plyer/pull/373) ([sandeepsajan0](https://github.com/sandeepsajan0))
- Update buildozer.spec [\#370](https://github.com/kivy/plyer/pull/370) ([sandeepsajan0](https://github.com/sandeepsajan0))
- Warn instead stder.write for linux notif errors [\#368](https://github.com/kivy/plyer/pull/368) ([sametmax](https://github.com/sametmax))
- Add coveralls.io report [\#367](https://github.com/kivy/plyer/pull/367) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix pep8 in plyer [\#366](https://github.com/kivy/plyer/pull/366) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- iOS Barometer API [\#363](https://github.com/kivy/plyer/pull/363) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Fix iOS Gyroscope crash issue [\#353](https://github.com/kivy/plyer/pull/353) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Keystore implementation. [\#351](https://github.com/kivy/plyer/pull/351) ([brentpicasso](https://github.com/brentpicasso))
- iOS Spatial orientation [\#348](https://github.com/kivy/plyer/pull/348) ([sumitmadhwani](https://github.com/sumitmadhwani))
- iOS Gravity sensor  [\#347](https://github.com/kivy/plyer/pull/347) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Linux Brightness API [\#346](https://github.com/kivy/plyer/pull/346) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Brightness API [\#344](https://github.com/kivy/plyer/pull/344) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Fix bug in WindowsBalloonTip [\#343](https://github.com/kivy/plyer/pull/343) ([Chronial](https://github.com/Chronial))
- Storage path API [\#342](https://github.com/kivy/plyer/pull/342) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Compass uncalibrated [\#341](https://github.com/kivy/plyer/pull/341) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Gyroscope uncalibrated sensor [\#337](https://github.com/kivy/plyer/pull/337) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Spatial Orientation for android [\#336](https://github.com/kivy/plyer/pull/336) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Update win\_api\_defs.py [\#335](https://github.com/kivy/plyer/pull/335) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Add some tests + Appveyor [\#329](https://github.com/kivy/plyer/pull/329) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Fix notification ticker error + pep8 [\#328](https://github.com/kivy/plyer/pull/328) ([KeyWeeUsr](https://github.com/KeyWeeUsr))
- Pep8 fix in temperature.py [\#322](https://github.com/kivy/plyer/pull/322) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Example for Unique ID facade [\#321](https://github.com/kivy/plyer/pull/321) ([sumitmadhwani](https://github.com/sumitmadhwani))
- Android Humidity [\#301](https://github.com/kivy/plyer/pull/301) ([bhaveshAn](https://github.com/bhaveshAn))
- fix handling of notifications' timeout on Linux [\#297](https://github.com/kivy/plyer/pull/297) ([benoit-pierre](https://github.com/benoit-pierre))
- Facade Wifi [\#290](https://github.com/kivy/plyer/pull/290) ([bhaveshAn](https://github.com/bhaveshAn))
- orientation feature for linux [\#273](https://github.com/kivy/plyer/pull/273) ([susmit](https://github.com/susmit))
- Fix wifi module. [\#244](https://github.com/kivy/plyer/pull/244) ([account-login](https://github.com/account-login))

## [1.3.0](https://github.com/kivy/plyer/tree/1.3.0) (2017-03-23)
[Full Changelog](https://github.com/kivy/plyer/compare/v1.2.4...1.3.0)

**Implemented enhancements:**

- Feature Request: Alarms [\#8](https://github.com/kivy/plyer/issues/8)

**Closed issues:**

- Notification.notify crashes android app  [\#296](https://github.com/kivy/plyer/issues/296)
- GPS android crash on launch [\#288](https://github.com/kivy/plyer/issues/288)
- Send SMS feature not working [\#261](https://github.com/kivy/plyer/issues/261)
- gps.configure\(\) results in exception [\#257](https://github.com/kivy/plyer/issues/257)
- v1.2.4 archive not available via github [\#234](https://github.com/kivy/plyer/issues/234)
- SyntaxError in wifi.py for Linux [\#230](https://github.com/kivy/plyer/issues/230)
- New PyPi release please, to fix static jfieldID not valid for class java.lang.Class\<org.renpy.android.PythonActivity\> [\#229](https://github.com/kivy/plyer/issues/229)
- Drag-and-drop: originate in Kivy, drop in some external app [\#228](https://github.com/kivy/plyer/issues/228)
- GPS Issue after in iOS after last changes in plyer [\#224](https://github.com/kivy/plyer/issues/224)
- battery.status isCharging always shows false [\#221](https://github.com/kivy/plyer/issues/221)
- GPS example only updating location once [\#217](https://github.com/kivy/plyer/issues/217)
- uniqueid.id raises exception on Windows [\#212](https://github.com/kivy/plyer/issues/212)
- Redundant libs folder [\#209](https://github.com/kivy/plyer/issues/209)
- accelerometer on Android with Kivy Launcher 1.9.0 not working [\#206](https://github.com/kivy/plyer/issues/206)
- Camera on android doesn't return to app [\#200](https://github.com/kivy/plyer/issues/200)
- android compass suggestion [\#195](https://github.com/kivy/plyer/issues/195)
- more example code to the docs [\#166](https://github.com/kivy/plyer/issues/166)
- Mail API on linux raises error NameError: name 'Email' is not defined [\#131](https://github.com/kivy/plyer/issues/131)
- native gui widgets [\#124](https://github.com/kivy/plyer/issues/124)
- android: using gps app cannot resume from pause [\#112](https://github.com/kivy/plyer/issues/112)
- Please upgrade pypi ! [\#94](https://github.com/kivy/plyer/issues/94)
- UniqueID using OpenID [\#83](https://github.com/kivy/plyer/issues/83)
- Display the notification in the right places [\#78](https://github.com/kivy/plyer/issues/78)
- Python3 All The Plyer! [\#12](https://github.com/kivy/plyer/issues/12)

**Merged pull requests:**

- Modify readme [\#308](https://github.com/kivy/plyer/pull/308) ([malverick](https://github.com/malverick))
- Add version tags in light and temperature facade [\#307](https://github.com/kivy/plyer/pull/307) ([malverick](https://github.com/malverick))
- Android ambient temperature sensor [\#293](https://github.com/kivy/plyer/pull/293) ([malverick](https://github.com/malverick))
- Android light sensor [\#292](https://github.com/kivy/plyer/pull/292) ([malverick](https://github.com/malverick))
- Plyer android proximity sensor [\#287](https://github.com/kivy/plyer/pull/287) ([malverick](https://github.com/malverick))
- Plyer android pressure sensor [\#286](https://github.com/kivy/plyer/pull/286) ([malverick](https://github.com/malverick))
- Update readme and plyer/\_\_init\_\_.py [\#285](https://github.com/kivy/plyer/pull/285) ([malverick](https://github.com/malverick))
- Plyer android gravity sensor [\#283](https://github.com/kivy/plyer/pull/283) ([malverick](https://github.com/malverick))
- Add on\_pause function [\#274](https://github.com/kivy/plyer/pull/274) ([malverick](https://github.com/malverick))
- uniqueid\_facade [\#270](https://github.com/kivy/plyer/pull/270) ([bhaveshAn](https://github.com/bhaveshAn))
- add bin and .buildozer directory to .gitignore [\#259](https://github.com/kivy/plyer/pull/259) ([malverick](https://github.com/malverick))
- pep8 fixes [\#250](https://github.com/kivy/plyer/pull/250) ([malverick](https://github.com/malverick))
- update code [\#249](https://github.com/kivy/plyer/pull/249) ([kiok46](https://github.com/kiok46))
- Adding small examples in facade files [\#237](https://github.com/kivy/plyer/pull/237) ([kiok46](https://github.com/kiok46))
- Fix TypeError if `LANG` is not set in on osx [\#232](https://github.com/kivy/plyer/pull/232) ([ForeverWintr](https://github.com/ForeverWintr))
- fix \#230 [\#231](https://github.com/kivy/plyer/pull/231) ([kiok46](https://github.com/kiok46))
- fix gps issue for ios [\#225](https://github.com/kivy/plyer/pull/225) ([kiok46](https://github.com/kiok46))
- Fixed issue \#221 [\#223](https://github.com/kivy/plyer/pull/223) ([Warlord77](https://github.com/Warlord77))
- Add flash example [\#219](https://github.com/kivy/plyer/pull/219) ([kiok46](https://github.com/kiok46))
- Make gps request parameters configurable [\#218](https://github.com/kivy/plyer/pull/218) ([kiok46](https://github.com/kiok46))
- Wifi Facade. OSX, Windows, Linux [\#213](https://github.com/kivy/plyer/pull/213) ([kiok46](https://github.com/kiok46))
- add sms for ios [\#203](https://github.com/kivy/plyer/pull/203) ([kiok46](https://github.com/kiok46))
- check android for namespace, otherwise use renpy [\#199](https://github.com/kivy/plyer/pull/199) ([kived](https://github.com/kived))
- fix p4a revamp [\#198](https://github.com/kivy/plyer/pull/198) ([kived](https://github.com/kived))
- Rewrite notification on Mac using PyOBJus [\#192](https://github.com/kivy/plyer/pull/192) ([andong777](https://github.com/andong777))
- Call for ios [\#191](https://github.com/kivy/plyer/pull/191) ([kiok46](https://github.com/kiok46))
- Note on requirements for iOS [\#187](https://github.com/kivy/plyer/pull/187) ([doratoa](https://github.com/doratoa))
- Adding battery example, notification ticker and gps example update [\#183](https://github.com/kivy/plyer/pull/183) ([kiok46](https://github.com/kiok46))
- Call and dial for android [\#181](https://github.com/kivy/plyer/pull/181) ([kiok46](https://github.com/kiok46))
- Dial or Call for android [\#180](https://github.com/kivy/plyer/pull/180) ([kiok46](https://github.com/kiok46))
- Added accuracy argument to on\_location call. [\#174](https://github.com/kivy/plyer/pull/174) ([lipi](https://github.com/lipi))
- Introduce camera access for ios and a example. [\#167](https://github.com/kivy/plyer/pull/167) ([akshayaurora](https://github.com/akshayaurora))
- macosx: fix incorrect method name in filechooser [\#165](https://github.com/kivy/plyer/pull/165) ([kived](https://github.com/kived))
- linux email import fix [\#151](https://github.com/kivy/plyer/pull/151) ([thegrymek](https://github.com/thegrymek))
- Merge android columns [\#148](https://github.com/kivy/plyer/pull/148) ([dessant](https://github.com/dessant))
- Camera example [\#41](https://github.com/kivy/plyer/pull/41) ([trivedigaurav](https://github.com/trivedigaurav))

## [v1.2.4](https://github.com/kivy/plyer/tree/v1.2.4) (2015-06-01)
[Full Changelog](https://github.com/kivy/plyer/compare/1.2.3...v1.2.4)

**Implemented enhancements:**

- Update platform check code [\#109](https://github.com/kivy/plyer/issues/109)

**Closed issues:**

- webhook test [\#142](https://github.com/kivy/plyer/issues/142)
- Sync style check updates from the Kivy repo [\#141](https://github.com/kivy/plyer/issues/141)
- GPS on android doesn't work \(a strange error\) [\#136](https://github.com/kivy/plyer/issues/136)
- Create toast notification facade for Android and iOS [\#126](https://github.com/kivy/plyer/issues/126)
- uniqueid.id empty on linux. [\#114](https://github.com/kivy/plyer/issues/114)
- Gyroscope Support for iOS [\#111](https://github.com/kivy/plyer/issues/111)
- AndroidUniqueID doesn't use Android ID [\#107](https://github.com/kivy/plyer/issues/107)
- OverflowError: Python int too large to convert to C long \[android lollipop\] [\#103](https://github.com/kivy/plyer/issues/103)
- Feature request: ability to open browser to a particular page [\#98](https://github.com/kivy/plyer/issues/98)
- AndroidGPS list GPS Provider but use hardcoded "gps" [\#54](https://github.com/kivy/plyer/issues/54)
- Email Support for Android \< 4.0 [\#42](https://github.com/kivy/plyer/issues/42)

**Merged pull requests:**

- style fixes [\#147](https://github.com/kivy/plyer/pull/147) ([dessant](https://github.com/dessant))
- add pydev files to gitignore [\#146](https://github.com/kivy/plyer/pull/146) ([dessant](https://github.com/dessant))
- Plyer style guide update [\#145](https://github.com/kivy/plyer/pull/145) ([thegrymek](https://github.com/thegrymek))
- Plyer audio for android with facade and example [\#144](https://github.com/kivy/plyer/pull/144) ([thegrymek](https://github.com/thegrymek))
- fix versionchanged tag [\#143](https://github.com/kivy/plyer/pull/143) ([dessant](https://github.com/dessant))
- update info about support email for android\<4.0 [\#140](https://github.com/kivy/plyer/pull/140) ([thegrymek](https://github.com/thegrymek))
- added plyer.facade to setuptools package [\#139](https://github.com/kivy/plyer/pull/139) ([thegrymek](https://github.com/thegrymek))
- splitted facades [\#138](https://github.com/kivy/plyer/pull/138) ([thegrymek](https://github.com/thegrymek))
- Inclement orientation [\#135](https://github.com/kivy/plyer/pull/135) ([thegrymek](https://github.com/thegrymek))
- remove unused variables [\#134](https://github.com/kivy/plyer/pull/134) ([thegrymek](https://github.com/thegrymek))
- fix \#107 - Use Android\_ID instead of IMEI [\#133](https://github.com/kivy/plyer/pull/133) ([aron-bordin](https://github.com/aron-bordin))
- vibrator for android v \< 4.0 [\#129](https://github.com/kivy/plyer/pull/129) ([thegrymek](https://github.com/thegrymek))
- PEP8 and typo fixes in MacOS X file chooser. [\#123](https://github.com/kivy/plyer/pull/123) ([robertjerovsek](https://github.com/robertjerovsek))
- pep8 - removed unused imports and variables [\#122](https://github.com/kivy/plyer/pull/122) ([thegrymek](https://github.com/thegrymek))
- Pep8 fix [\#121](https://github.com/kivy/plyer/pull/121) ([laltin](https://github.com/laltin))
- add video recoding to Camera facade and camera.py [\#120](https://github.com/kivy/plyer/pull/120) ([pspchucky](https://github.com/pspchucky))
- Use environ to change LANG to 'C' while calling shell processes [\#119](https://github.com/kivy/plyer/pull/119) ([trivedigaurav](https://github.com/trivedigaurav))
- add IrBlaster facade and Android implementation [\#118](https://github.com/kivy/plyer/pull/118) ([kived](https://github.com/kived))
- Android gps.py: fixed location provider cycling [\#117](https://github.com/kivy/plyer/pull/117) ([JimmyStavros](https://github.com/JimmyStavros))
- iOS GPS support [\#116](https://github.com/kivy/plyer/pull/116) ([laltin](https://github.com/laltin))
- use environ to change LANG to 'C' while calling lshw [\#115](https://github.com/kivy/plyer/pull/115) ([tshirtman](https://github.com/tshirtman))
- responds to issue 109 https://github.com/kivy/plyer/issues/109 [\#110](https://github.com/kivy/plyer/pull/110) ([AlbericC](https://github.com/AlbericC))
- Add file chooser facade and support for Linux and Windows [\#106](https://github.com/kivy/plyer/pull/106) ([Depaulicious](https://github.com/Depaulicious))

## [1.2.3](https://github.com/kivy/plyer/tree/1.2.3) (2015-01-27)
[Full Changelog](https://github.com/kivy/plyer/compare/1.2.2...1.2.3)

## [1.2.2](https://github.com/kivy/plyer/tree/1.2.2) (2015-01-27)
[Full Changelog](https://github.com/kivy/plyer/compare/1.2.1...1.2.2)

**Closed issues:**

- NotImplementedError: No usable implementation found! whith usable implementations on the system.  [\#108](https://github.com/kivy/plyer/issues/108)
- Gyro example [\#101](https://github.com/kivy/plyer/issues/101)
- Notification is not working in android [\#93](https://github.com/kivy/plyer/issues/93)
- plyer.notification.notfy\(\) raises NotImplementedError under Python 3.3 in Linux but not Python 2.7 [\#58](https://github.com/kivy/plyer/issues/58)

**Merged pull requests:**

- Linux platform check made compatible with python 3.3+ \(Fixes \#58\) [\#102](https://github.com/kivy/plyer/pull/102) ([helenst](https://github.com/helenst))

## [1.2.1](https://github.com/kivy/plyer/tree/1.2.1) (2014-08-19)
[Full Changelog](https://github.com/kivy/plyer/compare/1.2.0...1.2.1)

**Implemented enhancements:**

- Feature Request: codec-independent sound player [\#2](https://github.com/kivy/plyer/issues/2)

**Closed issues:**

- Battery status connected is actually isCharging [\#84](https://github.com/kivy/plyer/issues/84)
- Email Support for Windows [\#36](https://github.com/kivy/plyer/issues/36)
- Accelerometer Support for OSX [\#29](https://github.com/kivy/plyer/issues/29)
- Email Support for Linux [\#28](https://github.com/kivy/plyer/issues/28)
- Email Support for iOS [\#25](https://github.com/kivy/plyer/issues/25)
- TextToSpeech Support for iOS [\#24](https://github.com/kivy/plyer/issues/24)

**Merged pull requests:**

- fix print statement [\#92](https://github.com/kivy/plyer/pull/92) ([dessant](https://github.com/dessant))
- iOS UUID facade [\#90](https://github.com/kivy/plyer/pull/90) ([trivedigaurav](https://github.com/trivedigaurav))
- Removing build\_ext from plyer [\#89](https://github.com/kivy/plyer/pull/89) ([trivedigaurav](https://github.com/trivedigaurav))
- iOS Email Facade [\#88](https://github.com/kivy/plyer/pull/88) ([trivedigaurav](https://github.com/trivedigaurav))
- iOS Battery [\#86](https://github.com/kivy/plyer/pull/86) ([trivedigaurav](https://github.com/trivedigaurav))
- Change connected to isCharging [\#85](https://github.com/kivy/plyer/pull/85) ([trivedigaurav](https://github.com/trivedigaurav))
- Return None until sensor data is available [\#82](https://github.com/kivy/plyer/pull/82) ([trivedigaurav](https://github.com/trivedigaurav))
- Update compass.py [\#80](https://github.com/kivy/plyer/pull/80) ([ChrisCole42](https://github.com/ChrisCole42))
- Use whereis\_exe to check for binaries [\#79](https://github.com/kivy/plyer/pull/79) ([trivedigaurav](https://github.com/trivedigaurav))
- Update compass.py [\#77](https://github.com/kivy/plyer/pull/77) ([ChrisCole42](https://github.com/ChrisCole42))
- Maintenance [\#75](https://github.com/kivy/plyer/pull/75) ([trivedigaurav](https://github.com/trivedigaurav))
- facade docstring revision [\#74](https://github.com/kivy/plyer/pull/74) ([dessant](https://github.com/dessant))
- Query Battery info/status [\#73](https://github.com/kivy/plyer/pull/73) ([trivedigaurav](https://github.com/trivedigaurav))
- Revert "Activity was imported twice" [\#71](https://github.com/kivy/plyer/pull/71) ([trivedigaurav](https://github.com/trivedigaurav))
- Fix tabbing [\#70](https://github.com/kivy/plyer/pull/70) ([trivedigaurav](https://github.com/trivedigaurav))
- Gyroscope facade proxy declarations [\#69](https://github.com/kivy/plyer/pull/69) ([trivedigaurav](https://github.com/trivedigaurav))
- Linux accelerometer facade [\#68](https://github.com/kivy/plyer/pull/68) ([trivedigaurav](https://github.com/trivedigaurav))
- Update README.rst [\#67](https://github.com/kivy/plyer/pull/67) ([trivedigaurav](https://github.com/trivedigaurav))

## [1.2.0](https://github.com/kivy/plyer/tree/1.2.0) (2014-06-24)
**Implemented enhancements:**

- Feature Request: Add adjustable timeout option to Windows notification [\#13](https://github.com/kivy/plyer/issues/13)
- Changes notify to use ctypes instead of win32gui so we could use unicode. [\#18](https://github.com/kivy/plyer/pull/18) ([matham](https://github.com/matham))
- User-specified icon support for Windows notifications [\#11](https://github.com/kivy/plyer/pull/11) ([brousch](https://github.com/brousch))
- Added Vibrator facade and android implementation [\#6](https://github.com/kivy/plyer/pull/6) ([inclement](https://github.com/inclement))

**Closed issues:**

- GPS example crashes [\#40](https://github.com/kivy/plyer/issues/40)
- TextToSpeech Example App [\#20](https://github.com/kivy/plyer/issues/20)
- Accelerometer Example App [\#19](https://github.com/kivy/plyer/issues/19)

**Merged pull requests:**

- Plyer Unique ID facade [\#66](https://github.com/kivy/plyer/pull/66) ([trivedigaurav](https://github.com/trivedigaurav))
- Switched to pyjnius [\#63](https://github.com/kivy/plyer/pull/63) ([trivedigaurav](https://github.com/trivedigaurav))
- Update README [\#62](https://github.com/kivy/plyer/pull/62) ([trivedigaurav](https://github.com/trivedigaurav))
- Gyroscope Facades [\#60](https://github.com/kivy/plyer/pull/60) ([trivedigaurav](https://github.com/trivedigaurav))
- Ios compass [\#59](https://github.com/kivy/plyer/pull/59) ([trivedigaurav](https://github.com/trivedigaurav))
- Plyer compass facade [\#57](https://github.com/kivy/plyer/pull/57) ([trivedigaurav](https://github.com/trivedigaurav))
- Update README [\#56](https://github.com/kivy/plyer/pull/56) ([trivedigaurav](https://github.com/trivedigaurav))
- Using sudden motion sensor as accelerometer on OSX [\#55](https://github.com/kivy/plyer/pull/55) ([trivedigaurav](https://github.com/trivedigaurav))
- Added sms facade, example and android implementation [\#52](https://github.com/kivy/plyer/pull/52) ([mihaineacsu](https://github.com/mihaineacsu))
- add Mac OS X email support [\#49](https://github.com/kivy/plyer/pull/49) ([Depaulicious](https://github.com/Depaulicious))
- add Windows email support [\#48](https://github.com/kivy/plyer/pull/48) ([Depaulicious](https://github.com/Depaulicious))
- added Linux email support [\#47](https://github.com/kivy/plyer/pull/47) ([Depaulicious](https://github.com/Depaulicious))
- Add compat module, remove decoding of strings in notification [\#46](https://github.com/kivy/plyer/pull/46) ([matham](https://github.com/matham))
- Created an accelerometer example. Uses garden graph to plot the values [\#39](https://github.com/kivy/plyer/pull/39) ([trivedigaurav](https://github.com/trivedigaurav))
- Shows an error popup if there is no TTS [\#38](https://github.com/kivy/plyer/pull/38) ([trivedigaurav](https://github.com/trivedigaurav))
- Text to Speech Example [\#37](https://github.com/kivy/plyer/pull/37) ([trivedigaurav](https://github.com/trivedigaurav))
- readme typo corrected [\#15](https://github.com/kivy/plyer/pull/15) ([ghost](https://github.com/ghost))
- Introduce dbus notification [\#10](https://github.com/kivy/plyer/pull/10) ([akshayaurora](https://github.com/akshayaurora))
- Added an email facade and basic android implementation [\#5](https://github.com/kivy/plyer/pull/5) ([inclement](https://github.com/inclement))
- Tts [\#1](https://github.com/kivy/plyer/pull/1) ([brousch](https://github.com/brousch))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*