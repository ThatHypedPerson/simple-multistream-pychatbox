import socket
import json

login_file = open("twitch_login.json")
login = json.load(login_file)

twitch = socket.socket()
twitch.connect(('irc.chat.twitch.tv', 6667))
twitch.send(f"PASS {login['token']}\n".encode('utf-8'))
twitch.send(f"NICK {login['username']}\n".encode('utf-8'))
twitch.send(f"JOIN {login['channel']}\n".encode('utf-8'))

resp = twitch.recv(2048).decode('utf-8')
print(f"🟪 Twitch: Connected to {login['channel'][1:]}\n")

try:
    while True:
        resp = twitch.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            twitch.send('PONG\n'.encode('utf-8'))
        elif resp.startswith(":tmi.twitch.tv"):
            pass
        elif resp != "" and "PRIVMSG" in resp:
            username = resp[1 : resp.find("!")]
            message = resp[resp.find(" :") + 2 : -2]
            print(f"🟪 {username}: {message}")
except KeyboardInterrupt:
    twitch.close()
    print("Program exited.")