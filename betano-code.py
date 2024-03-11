import os
import json
import socket
import time
import random
import subprocess
import pyautogui

current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'configs' directory
CONFIG_DIR = os.path.join(current_directory, 'configs')

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def git_pull():
    try:
        subprocess.run(['git', 'pull'])
        print("Git pull completed successfully.")
    except Exception as e:
        print(f"Error during git pull: {e}")

# Git pull to update the local repository
git_pull()

# Load configuration files from the configs folder
configs = {}
for file_name in os.listdir(CONFIG_DIR):
    if file_name.endswith('.json'):
        file_path = os.path.join(CONFIG_DIR, file_name)
        config_name = os.path.splitext(file_name)[0]
        configs[config_name] = load_config(file_path)

# Print the menu of configurations
print("Available configurations:")
for index, config_name in enumerate(configs.keys(), 1):
    print(f"{index}) {config_name}")

# Select a config from the menu
selected_index = None
while not selected_index:
    try:
        selected_index = int(input("Enter the number of the configuration you want to use: "))
        if selected_index < 1 or selected_index > len(configs):
            print("Invalid selection. Please enter a number within the range.")
            selected_index = None
    except ValueError:
        print("Invalid input. Please enter a number.")

# Define variables from selected config
selected_config_name = list(configs.keys())[selected_index - 1]
config = configs[selected_config_name]

# Connect to Twitch IRC server
sock = socket.socket()
sock.connect((config['server'], config['port']))
sock.send(f"PASS {config['token']}\n".encode('utf-8'))
sock.send(f"NICK {config['nickname']}\n".encode('utf-8'))
sock.send(f"JOIN {config['channel']}\n".encode('utf-8'))

print("Script has started!")

# Initialize count variable, time of last action, and time of last message sent
word_count = 0
last_action_time = time.time()
last_message_sent_time = 0
reset_timer = time.time()  # Initialize the timer

# Main loop
while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    elif len(resp) > 0:
        # Split the message to extract the message content
        message_parts = resp.split(':', 2)
        if len(message_parts) >= 3:
            message_content = message_parts[2].lower()
            # Check if the message starts with "ADAMKO"
            if message_content.startswith('adamko') and not message_content.count('adamkosmesec') > 0:
                print("Received a message starting with 'ADAMKO':", message_content)
                # Search for windows containing "bonus" in their titles
                for window in pyautogui.getWindowsWithTitle('bonus'):
                    window.activate()
                    # Specify the coordinates of the local position where the click will occur
                    pyautogui.click(584, 323)
                    # Paste the message
                    pyautogui.write(message_content.strip())  # Assuming resp contains the promo code
                    pyautogui.press('enter')