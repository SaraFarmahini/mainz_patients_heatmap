import streamlit as st
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cm
from datetime import datetime, timedelta
import os
from streamlit_folium import folium_static
from postal_codes import POSTAL_CODE_COORDINATES

# Set page config
st.set_page_config(
    page_title="Mainz Patients Heatmap",
    page_icon="🏥",
    layout="wide"
)

# Load data with caching
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    try:
        df = pd.read_csv('monthly_postal_counts.csv')
        df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
        # Filter out postal codes not in our list
        valid_postal_codes = list(POSTAL_CODE_COORDINATES.keys())
        df = df[df['Postal Code'].astype(str).isin(valid_postal_codes)]
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
df = load_data()
if df is None:
    st.stop()

# Get unique dates (sorted)
dates = sorted(df['date'].unique())

# Create date slider (drag left/right for months)
selected_date = st.select_slider(
    "Select Month",
    options=dates,
    value=dates[0],
    format_func=lambda x: x.strftime("%B %Y")
)

# Filter data for selected date
df_selected = df[df['date'] == selected_date]

# Create the map
m = folium.Map(
    location=[49.9929, 8.2473],
    zoom_start=12,
    tiles='OpenStreetMap',
    control_scale=True
)

# Create a color map with more vibrant colors
max_patients = df_selected['Patient_Count'].max() if not df_selected.empty else 1
colormap = cm.LinearColormap(
    colors=['#1f77b4', '#2ca02c', '#ffd700', '#ff7f0e', '#d62728'],
    vmin=0,
    vmax=max_patients
)

# Add heatmap points with increased opacity
for _, row in df_selected.iterrows():
    postal_code = str(row['Postal Code'])
    count = row['Patient_Count']
    
    # Use actual coordinates from our postal code data
    if postal_code in POSTAL_CODE_COORDINATES:
        lat, lon = POSTAL_CODE_COORDINATES[postal_code]
        color = colormap(count)
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            popup=f'Postal Code: {postal_code}<br>Patients: {count}',
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            weight=2
        ).add_to(m)

# Add the color map to the map
colormap.add_to(m)

# Display the map using folium_static
folium_static(m, width=800, height=600)
