# SSH Manager

## Introduction

SSH Manager is a macOS menu bar application designed to manage SSH sessions efficiently. It allows users to store and manage multiple SSH sessions, categorized for easy access. It supports global and session-specific SSH keys, X11 forwarding, session search functionality, and automatic terminal integration with iTerm or macOS Terminal.

SSH Manager is packaged as a one-file executable using PyInstaller, and it stores configurations in JSON files that can be manually modified. The app also includes recent session tracking and mouse movement functionality to keep your system awake.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [File Locations](#file-locations)
- [Configuration](#configuration)
- [Global Parameter for SSH Key](#global-parameter-for-ssh-key)
- [Dependencies](#dependencies)
- [Examples](#examples)
- [Session File Builder](#session-file-builder)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

1. **Download the packaged executable:**
   - The app has been packaged as a single executable using PyInstaller. Download the executable and place it in a convenient location.

2. **Run the executable:**
   - Double-click the executable to start the SSH Manager.

3. **Ensure dependencies:**
   - Ensure that `osascript` is available on macOS for AppleScript commands and that you have a terminal application like iTerm or the default macOS Terminal installed.

## Usage

1. **Adding a session:**
   - Click on "Add Session" from the menu bar and input session details such as friendly name, connection string, category, and SSH key path (or use `none` for no key). After adding a session, you may need to restart SSH Manager.

2. **Connecting to a session:**
   - Select a session from the "Sessions" menu and click "Connect" to initiate an SSH session with the defined parameters.

3. **Transferring files via SCP:**
   - Select a session and click "Transfer" to transfer a file to the home directory of the target SSH session.

4. **Settings:**
   - Configure a global SSH key path, toggle X11 forwarding, and enable or disable mouse movement in the "Settings" menu.

5. **Recent sessions:**
   - Quickly reconnect to your 10 most recent sessions from the "Recent Sessions" menu.

6. **Mouse movement feature:**
   - Enable the "Mouse Move" setting to prevent the Mac from sleeping or appearing idle. This will randomly move the mouse to keep the system active.

7. **Searching sessions:**
   - Use the "Search Sessions" option to locate sessions by their friendly name.

8. **Restart after manual file intervention:**
   - Restart SSH Manager after manually modifying settings or sessions files.

## Features

- **Global SSH Key**: Use a global SSH key for all sessions, or specify individual keys for specific sessions.
- **X11 Forwarding**: Toggle X11 forwarding for graphical SSH applications.
- **Session Categories**: Organize SSH sessions into custom categories.
- **Session Search**: Quickly search for sessions by their friendly name.
- **Recent Sessions**: Track the 10 most recent sessions for quick access.
- **SCP File Transfer**: Transfer files via SCP to the home directory of a session.
- **Mouse Movement**: Enable random mouse movements to prevent the system from sleeping.
- **Permission Check**: Automatically set SSH key permissions to `600`.
- **Manual Configuration**: Modify session and settings files directly in JSON format.
- **Automatic Terminal Integration**: Open SSH sessions in iTerm or macOS Terminal.

## File Locations

- **Settings File**: `~/Documents/SSH_Manager/settings.txt`  
  Stores global SSH key path and X11 forwarding preferences in JSON format.

- **Sessions File**: `~/Documents/SSH_Manager/sessions.txt`  
  Stores session details such as the friendly name, connection string, category, etc. in JSON format.

Both files can be manually modified, but **restart SSH Manager** after making changes.

## Configuration

- **Global SSH Key**: Set a global SSH key to be used for all sessions unless a session-specific key is provided.
- **X11 Forwarding**: Enable X11 forwarding to allow graphical applications over SSH.
- **Mouse Movement**: Toggle the mouse movement feature to prevent the Mac from going idle.
- **Manual File Editing**: Session and settings files are in JSON format and can be edited directly. After manual changes, restart the application for updates to take effect.

## Global Parameter for SSH Key

When adding a session, if you wish to use the global SSH key, set the `ssh_key_path` value to `global`. Alternatively, use `none` if no SSH key is required for the session.

## Dependencies

- **Python** (only required if not packaged): Ensure Python 3 is installed on your system.
- **osascript**: Required for AppleScript commands to interact with dialogs and terminal applications.
- **iTerm** (optional): Recommended for users who prefer iTerm over macOS Terminal.

## Examples

### Adding a Session
- Friendly Name: e.g., "My Server"
- Connection String: e.g., `user@192.168.1.10`
- Category: e.g., "Work Servers"
- SSH Key Path: e.g., `/Users/yourname/.ssh/id_rsa`, `global` for the global SSH key, or `none` if no key is required.

### Connecting to a Session
- Select a session from the "Sessions" menu and click "Connect". The SSH connection will be opened in iTerm or Terminal based on your settings.

### File Transfer via SCP
- Select a session and click "Transfer" to choose a file for SCP transfer. The file will be transferred to the home directory of the session's target machine.

## Session File Builder

Use the provided `example_session_file_builder.xlsx` to simplify building the `sessions.txt` file. Fill in the details, copy the output from **Column D**, and paste it into `sessions.txt` within square brackets `[]`. Restart the app for the changes to take effect.

## Troubleshooting

- **Session or Settings Not Saving**: Ensure the `~/Documents/SSH_Manager` directory exists and is writable. Check file permissions.
- **Terminal Not Opening**: Make sure iTerm is installed, or SSH Manager will use the default Terminal app.
- **Manual File Edits Not Applied**: Restart the app after editing the settings or sessions files.

## Contributors

- **Lukas Nosalek** - Initial development

## License

This project is licensed under the Free License.
