import threading

import youtube
import twitch

youtube.init()

yt_chat = threading.Thread(target=youtube.messages)
ttv_chat = threading.Thread(target=twitch.messages)

yt_chat.start()
ttv_chat.start()