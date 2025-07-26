import os
import time
import pandas as pd

# ✅ Load simulated or fallback data
def load_simulated_data():
    file_path = "data/simulated_comments.csv"
    if not os.path.exists(file_path):
        print("[INFO] File not found, using fallback sample messages.")
        return pd.DataFrame({"message": [
            "You're awesome!",
            "This video sucks.",
            "Thanks for sharing!",
            "Worst video ever.",
        ]})
    return pd.read_csv(file_path)

# 🔁 Optional: stream messages every X seconds and pass to a callback
def stream_messages(callback, delay=10):
    while True:
        messages_df = load_simulated_data()
        callback(messages_df)
        time.sleep(delay)

