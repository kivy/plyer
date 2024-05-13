This is the process I used to compile my app for iOS. 
I used a virtualbox VM on a Windows 10 host running a macOS
Catalina guest (I couldn't get the newer ones to work without boot looping).
If you are running a macOS host with an M1 chip, you may have to use a Rosetta Terminal for
some of these steps, for more information, see:
https://nrodrig1.medium.com/how-to-run-your-kivy-app-on-your-iphone-5926e0917216
https://nrodrig1.medium.com/put-kivy-application-on-iphone-update-1cda12e79825

if you already have homebrew, Xcode (with command line tools), and python installed, you can skip to step 4. 

1. Install Homebrew (make sure to install Xcode command line tools when prompted):
<br>`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Install Python:
<br>`brew install python`
3. Install Xcode (I use version 13.4 because it is the last version that I can run on macOS Monterey). Extract this 
file in your application folder:
<br>https://developer.apple.com/services-account/download?path=/Developer_Tools/Xcode_13.4/Xcode_13.4.xip


4. Just a suggestion, make a directory for virtual environments and one for your projects:
```
mkdir ~/Documents/Environments
mkdir ~/Documents/kivy_builds
```
5. create and then activate a virtual environment:
```
cd kivy_builds
python -m venv venv_project_name`
source venv_projectP_name/bin/activate
```
6. Install kivy-ios prerequisites:
```
brew install autoconf automake libtool pkg-config
brew link libtool
```
7. Install your project requirements:
<br>`pip install -r requirements.txt`
8. Install kivy-ios:
<br>`pip install kivy-ios`
9. At the very least, your project will need kivy and python. I would recommend executing the following
command and copying the project folder to have a base to start from for subsequent projects. All you need to do is copy
the project folder and rename it, this will take a while to run:
<br>`toolchain build python3 kivy`
10. Some of your dependencies will need the build command, some will need pip install, you'll just have to 
figure out which ones need which:
```
toolchain build pillow numpy
toolchain pip install kivymd keyring requests
```
11. Create your project:
`toolchain create project_name /Users/$(whoami)/Documents/project_name`

The last command should create a project folder in your Documents folder named project_name-ios.
To compile the project, go into the directory and find the project_name.xcodeproj file. Open it with Xcode and from there
you can build it like any other Xcode project for iOS.