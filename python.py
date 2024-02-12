import os
import json
import socket
import time
import random
import subprocess

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return None

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def prompt_user_for_config():
    nickname = input("Enter your nickname: ")
    token = input("Enter your token: ")
    channel = "#" + input("Enter the channel name (e.g., 'respinnerstv'): ")
    word_to_detect = input("Enter the word to detect: ")
    count_threshold = int(input("Enter the count threshold: "))
    action_to_take = input("Enter word to send: ")
    repeat_input = input("Enter how many times you want the message to be written sequentially (0 for random between 1-5): ")
    cooldown_period = int(input("Enter how many seconds before sending the message in seconds: "))
    cooldown_after_send = int(input("Enter the cooldown period after sending the message in seconds: "))
    timer_reset_seconds = int(input("Enter the number of seconds for the timer reset: "))

    if repeat_input.isdigit():
        repeat = int(repeat_input)
        if repeat == 0:
            repeat = random.randint(1, 5)
    elif repeat_input.strip() == "":
        repeat = 1
    else:
        print("Invalid input. Please enter a valid number.")

    config = {
        "nickname": nickname,
        "token": token,
        "channel": channel,
        "word_to_detect": word_to_detect,
        "count_threshold": count_threshold,
        "action_to_take": action_to_take,
        "repeat": repeat,
        "cooldown_period": cooldown_period,
        "cooldown_after_send": cooldown_after_send,
        "timer_reset_seconds": timer_reset_seconds
    }

    save_config(config)
    return config

def git_pull():
    try:
        subprocess.run(['git', 'pull'])
        print("Git pull completed successfully.")
    except Exception as e:
        print(f"Error during git pull: {e}")

# Git pull to update the local repository
git_pull()

# Load configuration
config = load_config()

if config is None:
    print("Configuration file not found. Please provide the following details:")
    config = prompt_user_for_config()

# Define variables from config
server = 'irc.chat.twitch.tv'
port = 6667

# Connect to Twitch IRC server
sock = socket.socket()
sock.connect((server, port))
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
        # Count occurrences of the word to detect
        if resp.count(config['word_to_detect']) > 0:
            # Check if the cooldown period after sending the message has elapsed
            if time.time() - last_message_sent_time > config['cooldown_after_send']:
                word_count += 1

        # If the count threshold is reached or exceeded and cooldown period has elapsed
        if word_count >= config['count_threshold'] and time.time() - last_action_time >= config['cooldown_period']:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"{current_time} - Sent")
            # Send the specified action to the chat
            # Create the message by concatenating the action_to_take words
            message = " ".join([config['action_to_take'] for _ in range(config['repeat'])])
            # Send the message to the chat
            sock.send(f"PRIVMSG {config['channel']} :{message}\n".encode('utf-8'))
            # Reset the count and update time of last action and last message sent
            word_count = 0
            last_action_time = time.time()
            last_message_sent_time = time.time()
    
    # Reset the counter after the specified number of seconds
    if time.time() - reset_timer >= config['timer_reset_seconds']:
        word_count = 0
        reset_timer = time.time()
