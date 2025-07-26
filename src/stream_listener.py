import time
import pandas as pd

def load_simulated_data(file_path='data/sample_chat.csv'):
    df = pd.read_csv(file_path)
    return df['message'].tolist()

def stream_messages(messages, delay=1.0):
    for msg in messages:
        yield msg
        time.sleep(delay)