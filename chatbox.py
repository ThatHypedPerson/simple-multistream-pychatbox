import os
import time # delay api requests
import pprint # debugging print beautifier

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def displayLiveChatID(stream):  # change to getLiveChatId & remove liveChatId print when not debugging
    chat_id = stream['snippet']['liveChatId']
    print(f"Title: {stream['snippet']['title']}\nliveChatID: {chat_id}")
    print()
    return chat_id

# maybe seperate parts into different methods/functions
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Get all livestreams on the user's channel
    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails,status",
        broadcastStatus="all",
        broadcastType="all"
    )

    # cycle through all pages (might as well)
    streams = []
    while request is not None:
        response = request.execute()
        for item in response["items"]:
            if item["status"]["lifeCycleStatus"] != "complete": # only look at active/soon to be active streams
                streams.append(item)
        request = youtube.playlistItems().list_next(request, response)

    chat_id = "" # for use with LiveChatMessages

    # Debug print statements
    # pprint.pprint(streams)
    # print()
    # print(len(streams))

    if len(streams) == 1: # skip selection if theres only one stream selectable
        chat_id = displayLiveChatID(streams[0])
    else: # why would you have more than one stream available are you crazy
        index = 0
        for stream in streams:
            print(f"[{index}] {stream['snippet']['title']}")
            index += 1
        stream_choice = int(input("Choose which stream's liveChatId you want: "))
        chat_id = displayLiveChatID(streams[stream_choice])

    # check chat every 5-10 seconds (maybe do a wait for response["pollingIntervalMillis"])
    request = youtube.liveChatMessages().list(
        liveChatId=chat_id,
        part="snippet,authorDetails"
    )
    response = request.execute()

    # pprint.pprint(response) # Debug print statement
    # print()
    
    # 🟥: youtube
    # 🟪: twitch

    # # only display the current sent messages once
    # for message in response["items"]:
    #     print(f"{message['authorDetails']['displayName']}: {message['snippet']['displayMessage']}") # why are there two message fields in the response
    
    # maybe use a listener here instead of relying on KeyboardInterrupt
    message_ids = []
    try:
        while "error" not in response:
            for message in response["items"]:
                if message["id"] not in message_ids:
                    print(f"🟥 {message['authorDetails']['displayName']}: {message['snippet']['displayMessage']}") # why are there two message fields
                    message_ids.append(message["id"])
            time.sleep(response["pollingIntervalMillis"]/1000) if response["pollingIntervalMillis"]/1000 > 5 else time.sleep(5) # no idea if this works, maybe increase to 10
            response = request.execute()
    except KeyboardInterrupt:
        print("\nProgram Exited.")

if __name__ == "__main__":
    main()