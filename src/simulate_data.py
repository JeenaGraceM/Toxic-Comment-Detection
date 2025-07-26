import random
import pandas as pd

toxic_samples = [
    "You suck!",
    "I hate you!",
    "This is the worst stream ever.",
    "You're so dumb",
    "Kill yourself!",
    "Nobody likes you"
]

clean_samples = [
    "Wow, amazing gameplay!",
    "Keep it up!",
    "You're so talented!",
    "Love this stream!",
    "Awesome!",
    "This is fun"
]

data = [random.choice(toxic_samples + clean_samples) for _ in range(100)]
df = pd.DataFrame(data, columns=['message'])
df.to_csv("data/simulated_chat.csv", index=False)
print("Simulated chat saved to data/simulated_chat.csv")