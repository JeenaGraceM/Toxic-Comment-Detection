# stream_listener.py
from googleapiclient.discovery import build
import time
import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local development (optional)
load_dotenv()

# 🔐 Securely load API key and video ID
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY") or os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = st.secrets.get("VIDEO_ID") or os.getenv("VIDEO_ID")

# Check for required secrets
if not YOUTUBE_API_KEY:
    st.error("❌ YOUTUBE_API_KEY not found in Streamlit secrets or environment. Please set it.")
    st.stop()
if not VIDEO_ID:
    st.error("❌ VIDEO_ID not found. Please set it in Streamlit secrets or .env.")
    st.stop()

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

def stream_messages(delay=2):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    chat_id = get_live_chat_id(VIDEO_ID)

    if not chat_id:
        st.error("❌ Could not find live chat ID. Make sure the video is live and ID is correct.")
        return

    next_page_token = None

    while True:
        response = youtube.liveChatMessages().list(
            liveChatId=chat_id,
            part='snippet,authorDetails',
            pageToken=next_page_token
        ).execute()

        for item in response.get('items', []):
            message = item['snippet']['displayMessage']
            yield message

        next_page_token = response.get('nextPageToken')
        polling_interval = int(response.get('pollingIntervalMillis', 2000)) / 1000.0
        time.sleep(polling_interval)
