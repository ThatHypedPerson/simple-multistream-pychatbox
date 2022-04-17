from os import system, name # clear google authentication
import threading # run both chats at the same time

# Import external files + initialize their connections
import youtube
if name == 'nt': # Clear screen to make the output look nicer
    system('cls')
else:
    system('clear')

import twitch

# Get the YouTube livestream's chat
youtube.init()

# Set both chats to use threads
yt_chat = threading.Thread(target=youtube.messages)
ttv_chat = threading.Thread(target=twitch.messages)

# Start reading and printing from both chats
yt_chat.start()
ttv_chat.start()