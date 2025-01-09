# Kivy VOIP

## Table of Contents

- [Description](#description)
- [Usage](#usage)

## Description

Kivy VOIP is a simple, yet powerful framework designed for Kivy app developers to implement Voice Over IP (VOIP) functionality in their applications.
It simplifies the process of setting up voice communication between users, allowing developers to integrate it easily into their Kivy apps.
The main goal of this project is to provide a seamless VOIP experience, enabling direct communication between clients through an easily configurable server.
Caution must be exercised by the developer to prevent sending data to the wrong IP address or root domain.

Key features:
- Real-time voice communication.
- Includes SSL/TLS support.
- Easy integration with Kivy applications.
- Supports Android platforms.

## Usage

• To use the Kivy VOIP functionality, you will need to create a server application and configure it to route data sent by clients.
For testing purposes, the node VOIP server in this repository's example is configured to echo data back to a connected client.
Here is an outline of steps to run the node VOIP server from this repository:
1. Download "node VOIP server.js".
2. If not already installed, install node.js on your operating system.
3. If not already known, discover your server's local IP address by running "ipconfig" (Windows) or "ifconfig" (Linux) in your Command Line Interface (CLI).
   While the local port number is set to 8080 in the "node voip server.js" file, you can change it to any available port as desired.
4. Run the following command in your CLI to run the VOIP server when desired: node "node VOIP server.js". It is also possible to run the "node VOIP server.js"
   through VS Code.

• You will also need to create a client using the voip module. The main.py file in the main repository provides an example of how to utilize the voip.py module.
1. Download main.py and buildozer.spec.
2. In the start_call() function, update the dst_address and dst_port arguments in main.py to match your server's local IP address and port.
   All other arguements within the function are not required, but may be assigned values as desired.
3. Within your buildozer.spec file, ensure you have the following permissions before compiling with Buildozer:
   INTERNET, RECORD_AUDIO, ACCESS_NETWORK_STATE, and WAKE_LOCK.
4. Compile main.py with Buildozer to incorporate pyjnius into the mobile application by default.
5. Ensure the node VOIP server is running.
6. Ensure microphone permission is enabled for the compiled mobile application on your phone.
7. Run the compiled mobile application on your Android device and press the call button to hear your voice echoed back from the server.
