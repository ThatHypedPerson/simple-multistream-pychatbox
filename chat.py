from os import system, name # clear google authentication
import threading # run both chats at the same time

# Import external files + initialize their connections
import youtube
import twitch

if name == 'nt':
    system('cls')
else:
    system('clear')

# Get the YouTube livestream's chat
youtube.init()

# Set both chats to use threads
yt_chat = threading.Thread(target=youtube.messages)
ttv_chat = threading.Thread(target=twitch.messages)

# Start reading and printing from both chats
yt_chat.start()
ttv_chat.start()