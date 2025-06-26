#app.py
import streamlit as st
import pandas as pd

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("convo1.csv")  # <-- Make sure your file matches this name

df = load_data()

# Map from ID to row for fast lookup
id_map = {row["ID"]: row for _, row in df.iterrows()}

# Session state to track current conversation step
if "current_id" not in st.session_state:
    st.session_state.current_id = "Greeting"  # Starting point

# Get current step data
current_row = id_map.get(st.session_state.current_id)

if current_row:
    st.markdown(f"### {current_row['Message']}")

    col1, col2 = st.columns(2)

    # Show Option 1
    if pd.notna(current_row["Option 1 Text"]) and pd.notna(current_row["Option 1 Link"]):
        if col1.button(current_row["Option 1 Text"]):
            st.session_state.current_id = current_row["Option 1 Link"]
            st.experimental_rerun()

    # Show Option 2
    if pd.notna(current_row["Option 2 Text"]) and pd.notna(current_row["Option 2 Link"]):
        if col2.button(current_row["Option 2 Text"]):
            st.session_state.current_id = current_row["Option 2 Link"]
            st.experimental_rerun()

    # Reset button
    st.divider()
    if st.button("🔁 Restart Conversation"):
        st.session_state.current_id = "Greeting"
        st.experimental_rerun()

else:
    st.error("No matching step found. Please restart.")
    if st.button("Restart"):
        st.session_state.current_id = "Greeting"
        st.experimental_rerun()
