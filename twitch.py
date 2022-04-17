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

twitch.send('CAP REQ :twitch.tv/tags\n'.encode('utf-8')) # Get user badges in responses

while not (AttributeError, ConnectionResetError): # Just in case the connection has any issues from previous connections(?)
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
                # Add emojis before message based on chatter's status
                identifiers = "🟪 "
                badges = resp[resp.find("badges=") + 7 : resp.find(";", resp.find("badges=") + 1)]
                if(badges != ""):
                    if("broadcaster" in badges):
                        identifiers += "👑 "
                    if any(admin in badges for admin in ["admin", "global_mod", "staff"]): # no clue if these are correct
                        identifiers += "🛠️ "
                    if("moderator" in badges):
                        identifiers += "⚔️ "
                    if("vip" in badges):
                        identifiers += "💎 "
                    if("subscriber" in badges): # Maybe add different color stars based on subscriber status
                        identifiers += "⭐ "
                
                # Filter out someone's display name and message (dumb way of doing it, but it works)
                username = resp[resp.find("display-name=") + 13 : resp.find(";", resp.find("display-name="))]
                message = resp[resp.find(" :", resp.find("PRIVMSG")) + 2 : -2]
                print(f"{identifiers}{username}: {message}")
    except (SystemExit, KeyboardInterrupt): # Only stops on next message recieved
        twitch.close()
        print("\n🟪 Program exited.")

if __name__ == "__main__":
    messages()