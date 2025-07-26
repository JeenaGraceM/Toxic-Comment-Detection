import streamlit as st
from stream_listener import stream_messages
from preprocessing import clean_text
from classifier import classify_message

st.title("🛡️ Real-Time Toxic Comment Detection")

message_stream = stream_messages(delay=2)

for raw_msg in message_stream:
    cleaned = clean_text(raw_msg)
    result = classify_message(cleaned)
    toxic_score = result['Toxic']
    color = "red" if toxic_score > 0.5 else "green"
    st.markdown(f"<p style='color:{color}'>{raw_msg}</p>", unsafe_allow_html=True)
    st.json(result)
