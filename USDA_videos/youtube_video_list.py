import os
import json
import googleapiclient.discovery

def get_channel_videos(channel_id):
    """Fetches all videos from a YouTube channel and saves the data to a JSON file."""

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

import os
import json
import googleapiclient.discovery

def get_channel_videos(channel_id):
    """Fetches all videos from a YouTube channel and saves the data to a JSON file."""

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = input("Enter your YouTube Data API key: ")

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    channels_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []

    playlist_items_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    for item in playlist_items_response['items']:
        video_title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": video_title, "url": video_url})

    return videos


if __name__ == "__main__":
    channel_id = "UCUSDAAPHIS"  # USDA APHIS YouTube channel ID
    videos = get_channel_videos(channel_id)

    # Save the video data to a JSON file
    filepath = os.path.join(os.path.dirname(__file__), "videos.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)

    print(f"Video list saved to {filepath}")
