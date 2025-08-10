import streamlit as st
import pandas as pd
import time
from stream_listener import stream_messages
from preprocessing import clean_text
from classifier import classify_text
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- Page setup ---
st.set_page_config(page_title="🛡️ Toxic Comment Detector", layout="wide")
st.title("🧠 Real-Time Toxic Comment Detection Dashboard")

# --- Sidebar ---
st.sidebar.header("⚙️ Settings")
video_id = st.sidebar.text_input("🎥 YouTube Live Video ID", help="Paste the live YouTube video ID")
start_stream = st.sidebar.button("▶️ Start Monitoring")
enable_download = st.sidebar.checkbox("💾 Enable Download", value=True)

# --- Initialize DataFrame ---
if "results_df" not in st.session_state:
    st.session_state.results_df = pd.DataFrame(columns=["Message", "Label", "Toxicity", "Polarity", "Exclamations", "Length", "Time"])

results_df = st.session_state.results_df
chart_placeholder1 = st.empty()
chart_placeholder2 = st.empty()
chart_placeholder3 = st.empty()
message_container = st.container()

# --- Helper: draw charts ---
def draw_graphs(df):
    if df.empty:
        return

    with chart_placeholder1.container():
        st.subheader("📊 Toxic vs Non-Toxic")
        st.bar_chart(df["Label"].value_counts())

    with chart_placeholder2.container():
        st.subheader("📈 Toxicity Score Over Time")
        line_data = df[["Time", "Toxicity"]].set_index("Time")
        st.line_chart(line_data)

    with chart_placeholder3.container():
        st.subheader("🌀 Toxicity Distribution")
        pie_data = df["Label"].value_counts()
        fig, ax = plt.subplots(figsize=(2,2))
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# --- Streaming Chat ---
if start_stream and video_id:
    st.success(f"🚀 Monitoring video: `{video_id}`")

    toxic_count, nontoxic_count = 0, 0

    for msg in stream_messages(video_id):
        cleaned = clean_text(msg)
        result = classify_text(cleaned)

        # Data extraction
        toxic_score = result["probability_toxic"]
        label = "Toxic" if result["prediction"] == 1 else "Non-Toxic"
        polarity = round(TextBlob(cleaned).sentiment.polarity, 2)
        exclamations = msg.count("!")
        msg_len = len(msg)
        timestamp = pd.Timestamp.now().strftime("%H:%M:%S")

        # Save to session state
        new_row = pd.DataFrame([[msg, label, toxic_score, polarity, exclamations, msg_len, timestamp]],
                               columns=results_df.columns)
        st.session_state.results_df = pd.concat([st.session_state.results_df, new_row], ignore_index=True)
        results_df = st.session_state.results_df

        # Display
        with message_container:
            st.markdown(f"**[{label}]** `{msg}`")
            st.caption(f"🧪 Toxicity: {toxic_score:.2f} | 📏 Length: {msg_len} | ❗ Exclamations: {exclamations} | ⚖️ Polarity: {polarity}")

        # Update graphs
        draw_graphs(results_df)

        time.sleep(1.5)

    # Download button
    if enable_download and not results_df.empty:
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Chat Log", data=csv, file_name="chat_log.csv", mime="text/csv")

else:
    st.info("👈 Enter a valid YouTube Live Video ID and click **Start Monitoring**.")

# Show live stats always
if not results_df.empty:
    st.markdown("---")
    st.subheader("📋 Chat Log")
    st.dataframe(results_df.tail(10), use_container_width=True)
