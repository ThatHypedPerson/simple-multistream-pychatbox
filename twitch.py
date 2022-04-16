import socket
import json

# Get login information from a seperate json file
login_file = open("twitch_login.json")
login = json.load(login_file)

# Set up communications with Twitch's API
twitch = socket.socket()
twitch.connect(('irc.chat.twitch.tv', 6667))
twitch.send(f"PASS {login['token']}\n".encode('utf-8')) # OAuth
twitch.send(f"NICK {login['username']}\n".encode('utf-8')) # Username
twitch.send(f"JOIN {login['channel']}\n".encode('utf-8')) # Livestream's Channel Name

while not AttributeError: # Just in case the connection has any issues from previous connections(?)
    resp = twitch.recv(2048).decode('utf-8') # Check for a successful connection
print(f"🟪 Twitch: Connected to channel: {login['channel'][1:]}")

# Constantly check for new chat messages
def messages():
    try:
        print("🟪 Twitch: Now reading chat.")
        while True:
            resp = twitch.recv(2048).decode('utf-8')
            if resp.startswith('PING'): # Maintains connection with Twitch
                twitch.send('PONG\n'.encode('utf-8'))
            elif resp.startswith(":tmi.twitch.tv"): # Ignore other data sent by Twitch
                pass
            elif resp != "" and "PRIVMSG" in resp:
                username = resp[1 : resp.find("!")]
                message = resp[resp.find(" :") + 2 : -2]
                print(f"🟪 {username}: {message}")
    except (SystemExit, KeyboardInterrupt): # Only stops on next message recieved
        twitch.close()
        print("\n🟪 Program exited.")

if __name__ == "__main__":
    messages()