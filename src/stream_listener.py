# stream_listener.py
from googleapiclient.discovery import build
import time
import streamlit as st

import os
from dotenv import load_dotenv

YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY",None)
if not YOUTUBE_API_KEY:
    st.error("❌ YOUTUBE_API_KEY not found in Streamlit secrets. Please set it in the app settings.")
    st.stop()

# 🎥 Replace this with the actual live video ID (from YouTube URL)
VIDEO_ID = st.secrets.get("VIDEO_ID",None)

def get_live_chat_id(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()
    return response['items'][0]['liveStreamingDetails']['activeLiveChatId']

def stream_messages(delay=2):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    chat_id = get_live_chat_id(VIDEO_ID)
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
