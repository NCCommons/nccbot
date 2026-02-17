import os
import googleapiclient.discovery

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = input("Enter your YouTube Data API key: ")

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.channels().list(part="id,snippet", id="UCUSDAAPHIS")
response = request.execute()

print(response)
