import os
import time # delay api requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


# YouTube API setup

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
try:
    credentials = flow.run_console()
except Exception as error:
    print(error)
    quit()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


# Getting a stream's liveChatID to read messages
chat_id = ""
def displayLiveChatID(stream):
    global chat_id
    chat_id = stream['snippet']['liveChatId']
    print(f"🟥 Title: {stream['snippet']['title']}")
    # print(f"🟥 Title: {stream['snippet']['title']}\nliveChatID: {chat_id}") # debugging


# Get the livestream's chat we want to read from
def init():
    # Get all livestreams on the user's channel
    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails,status",
        broadcastStatus="all",
        broadcastType="all"
    )

    # cycle through all pages (might as well)
    streams = []
    try:
        while request is not None:
            response = request.execute()
            for item in response["items"]:
                if item["status"]["lifeCycleStatus"] != "complete": # only look at active/soon to be active streams
                    streams.append(item)
            request = youtube.playlistItems().list_next(request, response)
    except googleapiclient.errors.HttpError as error:
        reason = str(error)
        print(reason[reason.find("'message': '") + 12: reason.find("',", reason.find("'message': '"))])
        quit()
    except Exception as e:
        print("An unknown error has occcured.")
        print(e)
        quit()

    if len(streams) == 1: # skip selection if theres only one stream selectable
        displayLiveChatID(streams[0])
    elif len(streams) == 0: # if no livestreams are available on the channel
        print("There are no valid livestreams on this channel, exiting program.")
        quit()
    else: # why would you have more than one stream available are you crazy
        index = 0
        for stream in streams:
            print(f"[{index}] {stream['snippet']['title']}")
            index += 1
        stream_choice = int(input("Choose which stream's liveChatId you want: "))
        displayLiveChatID(streams[stream_choice])


# Constantly check for new chat messages
def messages():
    # Change request to look for messages in the livestream's chat
    request = youtube.liveChatMessages().list(
        liveChatId=chat_id,
        part="snippet,authorDetails"
    )
    response = request.execute()
    
    message_ids = []
    min_wait_time = 5 # Set to 10 to ensure the program can run 24/7 (why would you want that)
    # still need to check for when the amount of messages exceeds the first page
    try:
        print("🟥 YouTube: Now reading chat.")
        for message in response["items"]: # Ignore messages sent before running the program.
            message_ids.append(message["id"])
        while "error" not in response:
            for message in response["items"]:
                if message["id"] not in message_ids:
                    # Add emojis before message based on chatter's status
                    identifiers = "🟥 "
                    if message['authorDetails']['isChatOwner']:
                        identifiers += "👑"
                    if message['authorDetails']['isChatModerator']:
                        identifiers += "⚔️"
                    if message['authorDetails']['isChatSponsor']:
                        identifiers += "⭐"
                    if message['authorDetails']['isVerified']:
                        identifiers += "✔️"
                    username = message['authorDetails']['displayName']
                    text = message['snippet']['displayMessage']
                    if len(identifiers) > 2: # Add a space if a status is added to a message
                        identifiers += " "
                    print(f"{identifiers}{username}: {text}")

                    # Add message id to list so it does not get printed again
                    message_ids.append(message["id"])
            # wait until the request can be done again or 5 seconds to not fully use up the quota
            time.sleep(response["pollingIntervalMillis"]/1000) if response["pollingIntervalMillis"]/1000 > min_wait_time else time.sleep(min_wait_time)
            response = request.execute()
    except googleapiclient.errors.HttpError as error:
        if "liveChatEnded" in str(error):
            print("\n🟥 The livestream has ended, exiting chat.")
    except (SystemExit, KeyboardInterrupt):
        print("\n🟥 Program Exited.")
    except Exception as error:
        print("An unknown error has occured.")
        print(error)
        print("\n🟥 Program Exited.")
        quit()

if __name__ == "__main__":
    init()
    messages()