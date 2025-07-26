import os
import pandas as pd

def load_simulated_data():
    file_path = "data/simulated_comments.csv"
    if not os.path.exists(file_path):
        print("File not found, using fallback.")
        return pd.DataFrame({"message": [
            "You're awesome!",
            "This video sucks.",
            "Thanks for sharing!",
            "Worst video ever.",
        ]})
    return pd.read_csv(file_path)
