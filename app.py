import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

df = pd.read_csv("hud_properties.csv", encoding="ISO-8859-1")
df["property_id"] = df["property_id"].astype(str)

st.title("HUD Property Comp Selector")

subject_id = st.text_input("Enter Subject Property ID (to highlight):")

if subject_id and subject_id in df["property_id"].values:
    subject_row = df[df["property_id"] == subject_id].iloc[0]
    m = folium.Map(location=[subject_row["latitude"], subject_row["longitude"]], zoom_start=8)
    for _, row in df.iterrows():
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            continue
        popup = f"{row['property_name_text']} ({row['property_id']})"
        marker_color = "red" if row["property_id"] == subject_id else "blue"
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            icon=folium.Icon(color=marker_color)
        ).add_to(m)
    st_folium(m, width=800, height=600)

    # -------- Selection section ----------
    st.subheader("Select comps from the list below:")
    options = st.multiselect(
        "Choose properties (start typing name or ID):",
        df[df["property_id"] != subject_id].apply(lambda x: f"{x['property_name_text']} ({x['property_id']})", axis=1)
    )
    if options:
        selected_ids = [opt.split("(")[-1].replace(")", "") for opt in options]
        st.write("**Selected property IDs:**", selected_ids)
        st.download_button(
            "Download selected IDs as CSV",
            pd.DataFrame(selected_ids, columns=["property_id"]).to_csv(index=False),
            "selected_property_ids.csv"
        )
else:
    st.warning("Enter a valid property_id to view the map.")
