import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("hud_properties.csv")

st.title("🧪 Test: Print Subject Coordinates")

# Get user input
subject_id = st.text_input("Enter Subject Property ID")

if subject_id:
    try:
        # Ensure it's treated as a string
        subject_row = df[df["property_id"].astype(str) == str(subject_id)].iloc[0]
        lat = subject_row["latitude"]
        lon = subject_row["longitude"]
        st.write(f"📍 Latitude: {lat}")
        st.write(f"📍 Longitude: {lon}")
    except Exception as e:
        st.error(f"Could not retrieve coordinates: {e}")
