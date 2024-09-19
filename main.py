import os
import subprocess
import json
import rumps
import threading
import pyautogui
import random
from time import sleep


# Define the path to store settings and session files
def get_user_data_path():
    user_documents = os.path.expanduser("~/Documents/SSH_Manager")
    if not os.path.exists(user_documents):
        os.makedirs(user_documents)
    return user_documents

# Load sessions from file
def load_sessions():
    sessions_file = os.path.join(get_user_data_path(), 'sessions.txt')
    try:
        with open(sessions_file, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save sessions to file
def save_sessions(sessions):
    sessions_file = os.path.join(get_user_data_path(), 'sessions.txt')
    with open(sessions_file, 'w') as f:
        json.dump(sessions, f)

# Load recent sessions from file
def load_recent_sessions():
    recent_file = os.path.join(get_user_data_path(), 'recent_sessions.txt')
    try:
        with open(recent_file, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save recent sessions to file
def save_recent_sessions(recent_sessions):
    recent_file = os.path.join(get_user_data_path(), 'recent_sessions.txt')
    with open(recent_file, 'w') as f:
        json.dump(recent_sessions, f)

# Update the session list by adding the recent session, ensuring a maximum of 10 recent sessions
def update_recent_sessions(session):
    recent_sessions = load_recent_sessions()

    # Remove the session if it's already in the list to avoid duplicates
    recent_sessions = [s for s in recent_sessions if s['friendlyname'] != session['friendlyname']]

    # Add the session to the top of the list
    recent_sessions.insert(0, session)

    # Keep only the 10 most recent sessions
    if len(recent_sessions) > 10:
        recent_sessions = recent_sessions[:10]

    save_recent_sessions(recent_sessions)

# Load the global SSH key path and X11 forwarding setting
def load_ssh_key():
    settings_file = os.path.join(get_user_data_path(), 'settings.txt')
    try:
        with open(settings_file, 'r') as f:
            content = f.read().strip()
            if content:
                settings = json.loads(content)
                return settings.get('ssh_key', ''), settings.get('x11_forward', False)
            else:
                return "", False
    except FileNotFoundError:
        return "", False
    except json.JSONDecodeError:
        return "", False

def ensure_ssh_key_permissions(ssh_key_path):
    if os.path.exists(ssh_key_path):
        # Get the current permissions of the file
        file_stat = os.stat(ssh_key_path)
        file_permissions = oct(file_stat.st_mode)[-3:]

        # Check if the permissions are already 600, if not, change them
        if file_permissions != '600':
            try:
                os.chmod(ssh_key_path, 0o600)
            except Exception as e:
                print(f"Failed to set permissions for {ssh_key_path}: {str(e)}")


# Save the global SSH key path and X11 forwarding setting
def save_ssh_key_and_settings(ssh_key, x11_forward):
    settings_file = os.path.join(get_user_data_path(), 'settings.txt')
    settings = {'ssh_key': ssh_key, 'x11_forward': x11_forward}
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

# Use AppleScript to prompt for text input
def prompt_user(prompt_message, default_value=""):
    script = f'''
    try
        set user_input to text returned of (display dialog "{prompt_message}" default answer "{default_value}")
        return user_input
    on error
        return "CANCELED"
    end try
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() == "CANCELED":
        return None  # User canceled or error occurred
    return result.stdout.strip()

# Use AppleScript to prompt file selection
def prompt_file_choice():
    script = '''
    set chosenFile to choose file with prompt "Select a file for SCP transfer:"
    POSIX path of chosenFile
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None

# Build the SCP command and execute in iTerm or Terminal
def scp_file_transfer(session, global_ssh_key):
    file_path = prompt_file_choice()
    if file_path:
        connection_str = session['connection_string']
        ssh_key_path = session.get('ssh_key_path', '')

        # If session has no key, use the global key, or prompt for password if neither is available
        if ssh_key_path == "none":
            ssh_key_path = ""  # No SSH key path, will prompt for password
        elif "global" in ssh_key_path.lower():
            ssh_key_path = global_ssh_key
        
        if ssh_key_path:
            ensure_ssh_key_permissions(ssh_key_path)

        # Build the SCP command
        scp_command = f"scp"
        if ssh_key_path:
            scp_command += f" -i {ssh_key_path}"
        scp_command += f" {file_path} {connection_str}:~/"

        # Execute SCP in iTerm or Terminal
        try:
            if os.path.exists("/Applications/iTerm.app"):
                apple_script = f'''
                tell application "iTerm"
                    create window with default profile
                    tell current session of current window
                        write text "{scp_command}"
                    end tell
                end tell
                '''
                subprocess.run(['osascript', '-e', apple_script], check=True)
            else:
                apple_script = f'''
                tell application "Terminal"
                    do script "{scp_command}"
                    activate
                end tell
                '''
                subprocess.run(['osascript', '-e', apple_script], check=True)
        except Exception as e:
            rumps.alert(title="Error", message=f"Failed to open terminal: {str(e)}")
    else:
        rumps.alert("No file selected.")
        
# SSH connection function
def connect_to_ssh(session, global_ssh_key, x11_forward, remote_command=""):
    # Get connection string
    connection_str = session['connection_string']
    
    # Determine the SSH key path
    ssh_key_path = session.get('ssh_key_path', '')
    if ssh_key_path == "none":
        ssh_key_path = ""  # No key option if "none"
    elif "global" in ssh_key_path.lower():
        ssh_key_path = global_ssh_key  # Use global key if specified

    if ssh_key_path:
        ensure_ssh_key_permissions(ssh_key_path)

    # Build SSH command
    ssh_command = "ssh"
    
    # Add the -i option for SSH key if needed
    if ssh_key_path:
        ssh_command += f" -i {ssh_key_path}"

    # Add X11 forwarding if enabled
    if session.get('x11_forward', x11_forward):
        ssh_command += " -X"

    # Add the session connection string
    ssh_command += f" {connection_str}"
    
    # Add the optional remote command to run on the remote machine, if provided
    if remote_command:
        ssh_command += f" '{remote_command}'"
    
    # Execute the SSH command in iTerm or Terminal
    try:
        if os.path.exists("/Applications/iTerm.app"):
            apple_script = f'''
            tell application "iTerm"
                create window with default profile
                tell current session of current window
                    write text "{ssh_command}"
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', apple_script], check=True)
        else:
            apple_script = f'''
            tell application "Terminal"
                do script "{ssh_command}"
                activate
            end tell
            '''
            subprocess.run(['osascript', '-e', apple_script], check=True)
    except Exception as e:
        rumps.alert(title="Error", message=f"Failed to open terminal: {str(e)}")







# Create a class to handle the menu bar app using rumps
class SSHMenuBarApp(rumps.App):
    def __init__(self):
        super(SSHMenuBarApp, self).__init__("SSH", icon=None)
        self.sessions = load_sessions()
        self.recent_sessions = load_recent_sessions()  # Load recent sessions
        self.filtered_sessions = self.sessions
        #mouse move
        self.mouse_move_enabled = False
        self.mouse_mover_thread = None


        # Load global SSH key and X11 forwarding settings
        self.ssh_key, self.x11_forward = load_ssh_key()

        # Main menu items
        self.menu.add(rumps.MenuItem("Add Session", callback=self.add_session))
        # Create the settings submenu
        settings_menu = rumps.MenuItem("Settings")
        settings_menu.add(rumps.MenuItem("X11 Forwarding", callback=self.toggle_x11_forwarding))
        settings_menu.add(rumps.MenuItem("Global SSH Key", callback=self.change_global_ssh_key))
        settings_menu.add(rumps.MenuItem("Mouse Move", callback=self.toggle_mouse_movement))
        self.menu.add(settings_menu)
        #self.menu.add(rumps.MenuItem("Mouse Move", callback=self.toggle_mouse_movement))
        #self.menu.add(rumps.MenuItem("Settings", callback=self.open_settings))
        self.menu.add(rumps.MenuItem("Search Sessions", callback=self.search_sessions))

        # Add recent sessions submenu
        self.recent_sessions_menu = rumps.MenuItem("Recent Sessions")
        self.menu.add(self.recent_sessions_menu)

        # Add sessions submenu
        self.sessions_menu = rumps.MenuItem("Sessions")
        self.menu.add(self.sessions_menu)



        # Dynamically add session items
        self.refresh_sessions()

    # Toggle X11 forwarding setting
    def toggle_x11_forwarding(self, _):
        self.x11_forward = not self.x11_forward
        save_ssh_key_and_settings(self.ssh_key, self.x11_forward)
        rumps.alert("X11 Forwarding", "Enabled" if self.x11_forward else "Disabled")

    # Change the global SSH key
    def change_global_ssh_key(self, _):
        ssh_key = prompt_user("Enter the path to your SSH key:", default_value=self.ssh_key)
        if ssh_key:
            self.ssh_key = ssh_key
            save_ssh_key_and_settings(self.ssh_key, self.x11_forward)
            rumps.alert("Global SSH Key", f"Updated to {self.ssh_key}")
        
    def move_mouse(self):
        while self.mouse_move_enabled:
            sleep_time = random.uniform(5, 15)
            sleep(sleep_time)
            current_x, current_y = pyautogui.position()
            direction = random.randint(0, 1)
            distance = random.randint(100, 400)
        
            if direction == 0:
                new_y = max(current_y - distance, 20)  # Move up
            else:
                new_y = min(current_y + distance, 970)  # Move down
        
            pyautogui.moveTo(current_x, new_y, duration=0.25)

    def toggle_mouse_movement(self, _):
        if self.mouse_move_enabled:
            self.mouse_move_enabled = False
            if self.mouse_mover_thread and self.mouse_mover_thread.is_alive():
                self.mouse_mover_thread = None  # Stop the thread
            rumps.alert("Mouse movement stopped.")
        else:
            self.mouse_move_enabled = True
            self.mouse_mover_thread = threading.Thread(target=self.move_mouse)
            self.mouse_mover_thread.start()
            rumps.alert("Mouse movement started.")

    def refresh_sessions(self):
        # Clear previous session items in "Sessions" and "Recent Sessions"
        for key in list(self.menu["Sessions"].keys()):
            del self.menu["Sessions"][key]
        for key in list(self.menu["Recent Sessions"].keys()):
            del self.menu["Recent Sessions"][key]

        # Refresh recent sessions menu
        for session in self.recent_sessions:
            session_menu = rumps.MenuItem(session['friendlyname'])
            session_menu.add(rumps.MenuItem("Connect", callback=lambda sender, sess=session: self.connect_to_session(sess)))
            self.menu["Recent Sessions"].add(session_menu)

        # Group sessions by category
        categorized_sessions = {}
        for session in self.filtered_sessions:
            category = session.get('category', 'Uncategorized')
            if category not in categorized_sessions:
                categorized_sessions[category] = []
            categorized_sessions[category].append(session)

        # Add each session under its respective category, sorted alphabetically
        for category, sessions in categorized_sessions.items():
            # Sort sessions alphabetically by friendly name
            sorted_sessions = sorted(sessions, key=lambda s: s['friendlyname'].lower())
            
            category_menu = rumps.MenuItem(category)
            self.menu["Sessions"].add(category_menu)
            
            for session in sorted_sessions:
                session_menu = rumps.MenuItem(session['friendlyname'])
                session_menu.add(rumps.MenuItem("Connect", callback=lambda sender, sess=session: self.connect_to_session(sess)))
                session_menu.add(rumps.MenuItem("Transfer", callback=lambda sender, sess=session: self.scp_to_session(sess)))  # Add SCP option
                session_menu.add(rumps.MenuItem("Edit", callback=lambda sender, sess=session: self.edit_session(sess)))
                session_menu.add(rumps.MenuItem("Remove", callback=lambda sender, sess=session: self.remove_session(sess)))
                category_menu.add(session_menu)

    def connect_to_session(self, session):
        # Connect to SSH session and track it as recently accessed
        connect_to_ssh(session, self.ssh_key, self.x11_forward)
        update_recent_sessions(session)  # Update the recent session list
        self.recent_sessions = load_recent_sessions()  # Reload recent sessions
        self.refresh_sessions()

    def scp_to_session(self, session):
        scp_file_transfer(session, self.ssh_key)  # Perform SCP transfer to session

    def open_settings(self, _):
        # Prompt for SSH key path using osascript
        ssh_key = prompt_user("Enter the path to your SSH key:", default_value=self.ssh_key)
        if not ssh_key:
            return  # If user cancels the input or it's empty, do nothing

        # Prompt for X11 Forwarding option (simple yes/no dialog)
        x11_forward = rumps.alert("X11 Forwarding", "Enable X11 Forwarding?", ok="Yes", cancel="No") == 1

        # Save settings
        self.ssh_key = ssh_key
        self.x11_forward = x11_forward
        save_ssh_key_and_settings(self.ssh_key, self.x11_forward)

    def edit_session(self, session):
        friendlyname = prompt_user("Edit Friendly Name", session['friendlyname'])
        if friendlyname is None:
            return  # Cancel operation if the user cancels the input

        connection_string = prompt_user("Edit Connection String", session['connection_string'])
        if connection_string is None:
            return  # Cancel operation if the user cancels the input

        category = prompt_user("Edit Category", session.get('category', ''))
        if category is None:
            return  # Cancel operation if the user cancels the input

        ssh_key_path = prompt_user("Edit SSH Key Path (use 'none' for no key)", session.get('ssh_key_path', 'none'))
        if ssh_key_path is None:
            return  # Cancel operation if the user cancels the input

        # Save the updated session information
        session['friendlyname'] = friendlyname
        session['connection_string'] = connection_string
        session['category'] = category
        session['ssh_key_path'] = ssh_key_path if ssh_key_path else "none"
        save_sessions(self.sessions)
        self.filtered_sessions = self.sessions
        self.refresh_sessions()

    def remove_session(self, session):
        self.sessions = [s for s in self.sessions if s != session]
        save_sessions(self.sessions)
        self.filtered_sessions = self.sessions
        self.refresh_sessions()

    def add_session(self, _):
        # Collect all fields for the new session
        friendlyname = prompt_user("Enter Friendly Name")
        if friendlyname is None:
            return  # Cancel operation if the user cancels the input

        connection_string = prompt_user("Enter Connection String")
        if connection_string is None:
            return  # Cancel operation if the user cancels the input

        category = prompt_user("Enter Category")
        if category is None:
            return  # Cancel operation if the user cancels the input

        ssh_key_path = prompt_user("Enter SSH Key Path (use 'none' for no key)")
        if ssh_key_path is None:
            return  # Cancel operation if the user cancels the input

        # Save the new session if all inputs were provided
        if friendlyname and connection_string and category:
            self.sessions.append({
                'friendlyname': friendlyname,
                'connection_string': connection_string,
                'category': category,
                'ssh_key_path': ssh_key_path if ssh_key_path else "none"
            })
            save_sessions(self.sessions)
            self.filtered_sessions = self.sessions
            self.refresh_sessions()
        else:
            rumps.alert("Error", "Friendly name, connection string, and category are required.")

    def search_sessions(self, _):
        search_query = prompt_user("Enter search query").lower()
        if search_query:
            self.filtered_sessions = [session for session in self.sessions if search_query in session['friendlyname'].lower()]
        else:
            self.filtered_sessions = self.sessions
        self.refresh_sessions()


if __name__ == "__main__":
    SSHMenuBarApp().run()
