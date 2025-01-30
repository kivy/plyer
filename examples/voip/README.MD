# Kivy VoIP

## Table of Contents

- [Description](#description)
- [Server](#server)
- [Android](#android)
- [iOS](#iOS)

## Description

Kivy VoIP is a simple, yet powerful framework designed for Kivy app developers to implement Voice Over IP (VoIP) functionality in their applications.
It simplifies the process of setting up voice communication between users, allowing developers to integrate it easily into their Kivy apps.
The main goal of this project is to provide a seamless VoIP experience, enabling direct communication between clients through an easily configurable server.
Caution must be exercised by the developer to prevent sending data to the wrong IP address or root domain.

Key features:
- Real-time voice communication.
- Includes SSL/TLS support.
- Easy integration with Kivy applications.
- Supports Android and iOS platforms.

## Server

• To use the Kivy VoIP functionality, you will need to create a server application and configure it to route data sent by clients.
For testing purposes, the node VoIP server in this repository's example is configured to echo data back to a connected client.
Here is an outline of steps to run the node VoIP server from this repository:
1. Download "node VoIP server.js".
2. If not already installed, install node.js on your operating system.
3. If not already known, discover your server's local IP address by running "ipconfig" (Windows) or "ifconfig" (Linux) in your Command Line Interface (CLI).
   While the local port number is set to 8080 in the "node voip server.js" file, you can change it to any available port as desired.
4. Run the following command in your CLI to run the VoIP server when desired: node "node VoIP server.js". It is also possible to run the "node VoIP server.js"
   through VS Code.

## Android

1. Download main.py and buildozer.spec and place them in a folder that is solely used for this project.
2. Within the start_call() function, update the dst_address and dst_port arguments in main.py to match your server's local IP address and port.
   All other arguements within the function are not required but may be assigned values as desired.
3. Within your buildozer.spec file, ensure plyer is included.
4. Within your buildozer.spec file, also ensure you have the following permissions before compiling with Buildozer:
   INTERNET, RECORD_AUDIO, ACCESS_NETWORK_STATE, and WAKE_LOCK.
5. Compile main.py with Buildozer to incorporate pyjnius into the mobile application by default.
6. Ensure microphone permission is enabled for the compiled mobile application on your phone.
7. Ensure the node VoIP server is running.
8. Run the compiled mobile application on your Android device and press the call button to hear your voice echoing back from the server.

## iOS

• The VoIP iOS framework only supports arm_64 (actual iPhone) devices by default. To use the simulator, you must load the simulator
framework instead as commented in the voip.py source code located in the ios folder of the plyer module.
1. Download main.py and place it in a folder that is solely used for this project.
2. Within the start_call() function, update the dst_address and dst_port arguments in main.py to match your server's local IP address and port.
   All other arguements within the function are not required but may be assigned values as desired.
3. Through kivy-ios, utilize toolchain to create a new Xcode project that references the main.py folder.
4. Using toolchain, install plyer.
5. Open the project in Xcode and navigate to the project's directory explorer if not already selected.
6. Under resources, click yourprojectname-info to load the info.plist file of your project.
7. Hover over any description already set and press the add button to select "Privacy - Microphone Usage Description" to add microphone permission.
8. To the right of the permission, include a breif message to explain why microphone access is needed.
   This will appear during the permission request.
9. Ensure the node VoIP server is running.
10. Run the compiled mobile application on your iOS device and press the call button to hear your voice echoing back from the server.
