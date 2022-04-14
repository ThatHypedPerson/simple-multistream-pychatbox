import asyncio

import youtube
import twitch

yt = youtube.youtubeChat()
yt.init()

tw = twitch.twitchChat()

asyncio.run(yt.messages())
asyncio.run(tw.messages())