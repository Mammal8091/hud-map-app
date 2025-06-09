import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load and clean data
df = pd.read_csv("hud_properties.csv", encoding="ISO-8859-1")
df["property_id"] = df["property_id"].astype(str)

# Drop rows with missing or bad coordinates
df = df.dropna(subset=["latitude", "longitude"])
df = df[
    df["latitude"].apply(lambda x: isinstance(x, (float, int, float))) &
    df["longitude"].apply(lambda x: isinstance(x, (float, int, float)))
]

st.title("HUD Property Comp Selector")

subject_id = st.text_input("Enter Subject Property ID (to highlight):")

if subject_id:
    if subject_id in df["property_id"].values:
        subject_row = df[df["property_id"] == subject_id].iloc[0]

        if pd.isna(subject_row["latitude"]) or pd.isna(subject_row["longitude"]):
            st.error("Subject property is missing coordinates.")
            st.stop()

        m = folium.Map(location=[subject_row["latitude"], subject_row["longitude"]], zoom_start=8)

        for _, row in df.iterrows():
            popup = f"{row['property_name_text']} ({row['property_id']})"
            marker_color = "red" if row["property_id"] == subject_id else "blue"

            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=popup,
                icon=folium.Icon(color=marker_color)
            ).add_to(m)

        st_folium(m, width=800, height=600)
    else:
        st.warning("property_id not found. Check your input.")
else:
    st.warning("Enter a valid property_id to view the map.")
