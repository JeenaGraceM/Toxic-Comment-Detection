from googleapiclient.discovery import build
import time
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY") or os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    st.error("❌ YOUTUBE_API_KEY not found in Streamlit secrets or .env file.")
    st.stop()

# Get live chat ID from YouTube
def get_live_chat_id(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    items = response.get('items', [])
    if not items:
        return None
    return items[0].get('liveStreamingDetails', {}).get('activeLiveChatId')

# Stream chat messages
def stream_messages(video_id, delay=2):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    chat_id = get_live_chat_id(video_id)

    if not chat_id:
        st.error("❌ Could not find active chat. Make sure the video is live.")
        return

    next_page_token = None

    while True:
        response = youtube.liveChatMessages().list(
            liveChatId=chat_id,
            part='snippet,authorDetails',
            pageToken=next_page_token
        ).execute()

        for item in response.get('items', []):
            yield item['snippet']['displayMessage']

        next_page_token = response.get('nextPageToken')
        polling_interval = int(response.get('pollingIntervalMillis', 2000)) / 1000.0
        time.sleep(polling_interval)
