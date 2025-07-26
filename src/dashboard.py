import streamlit as st
from stream_listener import load_simulated_data, stream_messages
from preprocessing import clean_text
from classifier import classify_message

st.set_page_config(page_title="Toxic Comment Detection", layout="centered")
st.title("🛡️ Real-Time Toxic Comment Detection")

# Callback function to process & display messages
def display_messages(messages_df):
    st.subheader("Live Chat Monitoring")

    for raw_msg in messages_df["message"]:
        cleaned = clean_text(raw_msg)
        result = classify_message(cleaned)
        toxic_score = result.get("Toxic", 0)
        color = "red" if toxic_score > 0.5 else "green"

        st.markdown(f"<p style='color:{color}; font-size:16px'>{raw_msg}</p>", unsafe_allow_html=True)
        st.json(result)

# 👉 Option A: Stream messages repeatedly (only if you're running locally or using auto-refresh)
# stream_messages(display_messages, delay=2)

# 👉 Option B: Load once and display (recommended for Streamlit Cloud)
messages_df = load_simulated_data()
display_messages(messages_df)
