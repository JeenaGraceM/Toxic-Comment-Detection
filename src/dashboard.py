import streamlit as st
from stream_listener import stream_messages  # Removed load_simulated_data
from preprocessing import clean_text
from classifier import classify_message

st.set_page_config(page_title="Toxic Comment Detection", layout="centered")
st.title("🛡️ Real-Time Toxic Comment Detection")

st.subheader("Live Chat Monitoring")

# Container for displaying messages dynamically
message_container = st.container()

# Start streaming messages from YouTube Live Chat
for raw_msg in stream_messages():
    cleaned = clean_text(raw_msg)
    result = classify_message(cleaned)
    toxic_score = result.get("Toxic", 0)
    color = "red" if toxic_score > 0.5 else "green"

    with message_container:
        st.markdown(f"<p style='color:{color}; font-size:16px'>{raw_msg}</p>", unsafe_allow_html=True)
        st.json(result)
