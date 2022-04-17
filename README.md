# Simple Multistream Python Chatbox

I made this just to learn how the chats for both YouTube and Twitch livestreaming work for a different project. This will not send any messages, only read and print them to the terminal.<br>
This was made in Python 3.10, so I have no idea if its backwards compatible.

# Setup
## Prerequisites
You need to set up a project using [Google's YouTube API](https://developers.google.com/youtube/v3/quickstart/python) and install [Google's Python API Libraries](https://developers.google.com/youtube/v3/quickstart/python#prerequisites) or use the `requirements.txt` file by running `pip install -r requirements.txt` to install the required libraries.<br>
You also need a Twitch OAuth key, which you can get from https://twitchapps.com/tmi/.

## Authentication
You need to have to files in the same folder in order to connect to each service. Every time you run the program you need to follow the link and put in an authorization code (I need to find a way to skip this step).
### **YouTube**
Download the `client_secret_#########.json` file and rename it to `client_secret.json`.
### **Twitch**
Create the file `twitch_login.json` and include the following structure.
```
{
    "token":"oauth:OAUTHTOKEN",
    "channel":"#CHANNEL",
    "username":"NAME"
}
```
* `"token"` is the OAuth token you get from https://twitchapps.com/tmi/.
* `"channel"` is the name of the livestream's chat you want to read from, for example `"channel":"#thathypedperson"`.
* `"username"` is the same username you used to get the OAuth token (i think), for example `"username":"thathypedperson"`.
### **Structure**
With every file added properly, your folder should look like this (excluding git files).
```
simple-multistream-pychatbox/
    chat.py
    client_secret.json
    twitch_login.json
    twitch.py
    youtube.py
```

# Usage
This program does not support any arguments. Just run the file `chat.py` normally.
```
python chat.py
```
* You will need to follow the link put in the output to get an authorization code from Google before the program can run.
### **A YouTube Channel Has Multiple Streams**
(Untested) You will be prompted to choose a stream to read the chat from.
```
[0] Stream 1
[1] Stream 2
Choose which stream's liveChatId you want: 
```
# To-Do/Known Issues
* The YouTube livestream chat will only read up to one "page" (returned from the request, one page only holds a certain amount of messages), need to add a way to go to the next page once it is full.
* This program only reads chat messages from one YouTube livestream and one Twitch Livestream, I may add a way to set this up using arguments or a way to add more streams.
* A way to skip Google Authentication needing to be ran every time, this should be a simple fix for reading from the same stream.
* An argument to disable the printing of emojis. Emojis are currently used to show a user's identifiers/badges (broadcaster/mod/vip) or in some messages, but some terminals can't output emojis.
* Rate limiting - encountered some issues with this during programming, but they shouldn't come up during use. (If left running all day, YouTube may run out of queries)
* The way the program displays YouTube chat is sloppy, need to find a better way of choosing which messages to display.
* Commands on Twitch do not print correctly.
* There will be no way to remove deleted messages from the output.