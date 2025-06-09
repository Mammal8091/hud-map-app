import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Load HUD property data
df = pd.read_csv("hud_properties.csv", encoding="utf-8", errors="replace")

# Streamlit layout
st.set_page_config(layout="wide")
st.title("HUD Property Comp Selector")

subject_id = st.text_input("Enter Subject Property ID (to highlight):")

# Initialize map
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

selected_ids = []

for _, row in df.iterrows():
    marker_color = "red" if str(row["property_id"]) == subject_id else "blue"
    popup = f"{row['property_name_text']}<br>{row['address_line1_text']}<br>{row['city_name_text']}, {row['state_code']}"
    
    marker = folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup,
        icon=folium.Icon(color=marker_color)
    )
    marker.add_to(marker_cluster)

# Render map and capture clicks
output = st_folium(m, width=1200, height=600)

if output and "last_object_clicked" in output:
    latlon = output["last_object_clicked"]
    match = df[(df["latitude"] == latlon["lat"]) & (df["longitude"] == latlon["lng"])]
    if not match.empty:
        pid = match.iloc[0]["property_id"]
        if pid not in selected_ids:
            selected_ids.append(pid)

# Show selected property_ids
if selected_ids:
    st.write("✅ Selected Property IDs:")
    st.code(", ".join(map(str, selected_ids)))
