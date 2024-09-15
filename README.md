# SSH Manager

## Introduction

SSH Manager is a macOS menu bar application designed to manage SSH sessions efficiently. It allows users to store and manage multiple SSH sessions, categorized for easy access. It also supports global and session-specific SSH keys, as well as X11 forwarding. The app can be configured to use a global SSH key for all sessions, or individual keys for specific sessions. It also offers a search functionality to quickly locate sessions.

This project is packaged as a one-file executable (SSH Manager) using PyInstaller, and stores configuration in JSON files that can be manually modified.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [File Locations](#file-locations)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

1. **Download the packaged executable:**
   - The app has been packaged as a single executable using PyInstaller. You can download the executable and place it in a convenient location.

2. **Run the executable:**
   - Simply double-click the executable to start the SSH Manager.
   
3. **Ensure dependencies:**
   - Make sure that macOS has `osascript` available for AppleScript commands and a terminal application like iTerm or macOS Terminal.

## Usage

1. **Adding a session:**
   - From the menu bar, click on "Add Session" to input the session details such as the friendly name, connection string, category, and SSH key path (or use `none` for no key). If this is your first time adding a session, SSH Manager will need to be restarted.

2. **Connecting to a session:**
   - From the "Sessions" menu, select a session and click "Connect" to start an SSH session using the predefined parameters.

3. **Settings:**
   - Configure a global SSH key path and enable or disable X11 forwarding through the "Settings" option.

4. **Searching sessions:**
   - Use the "Search Sessions" option to quickly find a session by its friendly name.

5. **Restart the app after manual file intervention:**
   - If you manually modify the settings or sessions files, **restart the SSH Manager** for the changes to take effect.

## Features

- **Global SSH Key**: Use a global SSH key for all sessions or specify individual keys for specific sessions.
- **X11 Forwarding**: Toggle X11 forwarding for graphical applications over SSH.
- **Session Categories**: Organize SSH sessions into custom categories.
- **Session Search**: Quickly search for sessions by name.
- **Manual Configuration**: Modify sessions and settings files manually if needed.
- **Automatic Terminal Integration**: Automatically open SSH sessions in iTerm or macOS Terminal.

## File Locations

The application stores its configuration and session data in the following locations:

- **Settings File**: `~/Documents/SSH_Manager/settings.txt`
  - Contains global SSH key path and X11 forwarding preferences.
  - Stores JSON format.

- **Sessions File**: `~/Documents/SSH_Manager/sessions.txt`
  - Contains session details (friendly name, connection string, category, etc.).
  - Stores JSON format.

Both files can be manually modified if required, but **the app must be restarted** for the changes to take effect.

## Configuration

- **Global SSH Key**: You can set a global SSH key that will be used for all sessions unless a session-specific key is defined.
- **X11 Forwarding**: Enable X11 forwarding for graphical SSH applications.
- **Manual File Editing**: Settings and session files are stored as JSON and can be modified manually. Make sure to restart the application after manual changes.

## Dependencies

The app requires the following to be installed on macOS:

- **Python** (if not packaged as a single file): Ensure Python 3 is installed.
- **osascript**: The application uses AppleScript for dialogs and controlling terminal applications.
- **iTerm** (optional): For users who prefer iTerm over the default macOS Terminal.

## Examples

### Adding a Session
When you click "Add Session", you'll be prompted to enter:
- Friendly name: e.g., "My Server"
- Connection string: e.g., `user@192.168.1.10`
- Category: e.g., "Work Servers"
- SSH key path: e.g., `/Users/yourname/.ssh/id_rsa`, or `none` if no key is required.

### Connecting to a Session
Once a session is added, select it from the "Sessions" menu and click "Connect". The SSH connection will open in iTerm or Terminal based on your configuration.

## Troubleshooting

- **Session or Settings Not Saving**: Ensure that the `~/Documents/SSH_Manager` directory exists and is writable. Check file permissions if settings or sessions are not being saved.
- **Terminal Not Opening**: If iTerm is not installed, the app will fall back to the macOS default Terminal. Ensure that at least one terminal application is installed and accessible.
- **Manual File Edits Not Applied**: Restart the app after making manual changes to `settings.txt` or `sessions.txt`.

## Contributors

- **Lukas Nosalek** - Initial development

## License

This project is licensed under the Free License
