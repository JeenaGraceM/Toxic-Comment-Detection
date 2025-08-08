import streamlit as st
import pandas as pd
import time
from stream_listener import stream_messages
from preprocessing import clean_text
from classifier import classify_text  # ✅ using the hybrid model now

# Streamlit layout
st.set_page_config(page_title="Toxic Comment Detection", layout="wide")
st.title("🛡️ Real-Time Toxic Comment Detection")

# Sidebar for settings
st.sidebar.header("🔧 Configuration")
video_id = st.sidebar.text_input("Enter YouTube Live Video ID", value="", help="Paste the YouTube live video ID here")
start_stream = st.sidebar.button("▶️ Start Monitoring")
show_graphs = st.sidebar.checkbox("📊 Show Visualizations", value=True)
download_log = st.sidebar.checkbox("💾 Enable Download", value=True)

# Layout placeholders
col1, col2 = st.columns(2)
message_container = st.container()
chart_placeholder = st.empty()

# Store results
results_df = pd.DataFrame(columns=["message", "label", "toxic_score"])

# Start processing if input is provided
if start_stream and video_id:
    st.success("✅ Streaming started. Fetching comments from video ID: " + video_id)
    toxic_count, nontoxic_count = 0, 0

    for raw_msg in stream_messages(video_id):
        cleaned = clean_text(raw_msg)
        result = classify_text(cleaned)  # ✅ use hybrid model
        toxic_score = result["probability_toxic"]
        label = "Toxic" if result["prediction"] == 1 else "Non-Toxic"

        # Count update
        if label == "Toxic":
            toxic_count += 1
        else:
            nontoxic_count += 1

        # Save result
        results_df.loc[len(results_df)] = [raw_msg, label, toxic_score]

        # Display message and score
        with message_container:
            st.write(f"{label} Message: {raw_msg}")
            st.json(result)

        # Update metrics
        col1.metric("☣️ Toxic Comments", toxic_count)
        col2.metric("✅ Non-Toxic Comments", nontoxic_count)

        # Graph update
        if show_graphs:
            chart_data = pd.DataFrame({
                "Labels": ["Toxic", "Non-Toxic"],
                "Counts": [toxic_count, nontoxic_count]
            })
            chart_placeholder.bar_chart(chart_data.set_index("Labels"))

        time.sleep(1.5)

    # Download results
    if download_log and not results_df.empty:
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Chat Log", data=csv, file_name="chat_log.csv", mime='text/csv')
else:
    st.info("Please enter a valid YouTube Live Video ID and click 'Start Monitoring'.")
