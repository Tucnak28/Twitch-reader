import socket
import time
import random
import subprocess

# Git pull to update the local repository
try:
    subprocess.run(['git', 'pull'])
    print("Git pull completed successfully.")
except Exception as e:
    print(f"Error during git pull: {e}")
    
# Define variables
server = 'irc.chat.twitch.tv'
port = 6667

# Prompt the user for variable values

nickname = input("Enter your nickname: ")
token = input("enter your token: ")
channel = "#" + input("Enter the channel name (e.g., 'respinnerstv'): ")
word_to_detect = input("Enter the word to detect: ")
count_threshold = int(input("Enter the count threshold: "))
action_to_take = input("Enter word to send: ")
repeat_input = input("Enter how many times you want the message to be written sequentially (0 for random between 1-5): ")
cooldown_period = int(input("Enter how many seconds before sending the message in seconds: "))
cooldown_after_send = int(input("Enter the cooldown period after sending the message in seconds: "))

# Check if the input is numeric
if repeat_input.isdigit():
    repeat = int(repeat_input)
    if repeat == 0:
        # If the input is 0, generate a random number between 1 and 5
        repeat = random.randint(1, 5)
elif repeat_input.strip() == "":
    # If the input is empty, use default value 1
    repeat = 1
else:
    # If the input is not numeric, prompt the user again
    print("Invalid input. Please enter a valid number.")

# Connect to Twitch IRC server
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

print("Script has started!")

# Initialize count variable, time of last action, and time of last message sent
word_count = 0
last_action_time = time.time()
last_message_sent_time = 0

# Main loop
while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    elif len(resp) > 0:
        # Count occurrences of the word to detect
        if(resp.count(word_to_detect) > 0):
            # Check if the cooldown period after sending the message has elapsed
            if time.time() - last_message_sent_time > cooldown_after_send:
                word_count += 1

        # If the count threshold is reached or exceeded and cooldown period has elapsed
        if word_count >= count_threshold and time.time() - last_action_time >= cooldown_period:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"{current_time} - Sent")
            # Send the specified action to the chat
            # Create the message by concatenating the action_to_take words
            message = " ".join([action_to_take for _ in range(repeat)])
            # Send the message to the chat
            sock.send(f"PRIVMSG {channel} :{message}\n".encode('utf-8'))
            # Reset the count and update time of last action and last message sent
            word_count = 0
            last_action_time = time.time()
            last_message_sent_time = time.time()
