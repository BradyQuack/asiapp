import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Conversation Flow", layout="wide")

# Load CSV file with caching
@st.cache_data
def load_data():
    return pd.read_csv("convo1.csv")  # Ensure this file is in the same directory

df = load_data()

# Build a dictionary mapping each ID to its row for fast access
id_map = {row["ID"]: row for _, row in df.iterrows()}

# Initialize session state to track where we are in the conversation
if "current_id" not in st.session_state:
    st.session_state.current_id = "Greeting"  # Starting point of the conversation

# Get the current row based on session state
current_row = id_map.get(st.session_state.current_id)

# Main UI
st.title("Plumber Script")

if current_row is not None:
    st.markdown(f"## {st.session_state.current_id}")
    st.markdown(f"### {current_row['Message']}")

    col1, col2 = st.columns(2)

    # Option 1 button
    if pd.notna(current_row["Option 1 Text"]) and pd.notna(current_row["Option 1 Link"]):
        if col1.button(current_row["Option 1 Text"]):
            st.session_state.current_id = current_row["Option 1 Link"]
            st.rerun()

    # Option 2 button
    if pd.notna(current_row["Option 2 Text"]) and pd.notna(current_row["Option 2 Link"]):
        if col2.button(current_row["Option 2 Text"]):
            st.session_state.current_id = current_row["Option 2 Link"]
            st.rerun()

    # Divider + Reset
    st.divider()
    if st.button("🔁 Restart Conversation"):
        st.session_state.current_id = "Greeting"
        st.rerun()

else:
    st.session_state.current_id = "Greeting"
    st.rerun()
