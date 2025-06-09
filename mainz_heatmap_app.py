import streamlit as st
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cm
from datetime import datetime, timedelta
import os
from streamlit_folium import folium_static

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
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
df = load_data()
if df is None:
    st.stop()

# Get unique dates
dates = sorted(df['date'].unique())

# Create date selector
selected_date = st.selectbox(
    "Select Date",
    options=dates,
    format_func=lambda x: x.strftime("%B %Y"),
    index=0
)

# Filter data
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
    
    # Approximate coordinates based on postal code
    lat = 49.9929 + (int(postal_code[-2:]) - 16) * 0.005
    lon = 8.2473 + (int(postal_code[-2:]) - 16) * 0.005
    
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