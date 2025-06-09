import streamlit as st
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cm
from datetime import datetime, timedelta
import os
from streamlit_folium import folium_static

# Clear all caches
st.cache_data.clear()
st.cache_resource.clear()

# Set page config for better performance
st.set_page_config(
    page_title="Mainz Patients Heatmap",
    page_icon="🏥",
    layout="wide"
)

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password.
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Load data with caching
    @st.cache_data
    def load_data():
        df = pd.read_csv('monthly_postal_counts.csv')
        # Create date column from Year and Month
        df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
        return df

    df = load_data()
    
    # Get unique dates for the slider
    dates = sorted(df['date'].unique())
    
    # Create date range slider
    selected_date = st.select_slider(
        "Select Date",
        options=dates,
        format_func=lambda x: x.strftime("%B %Y"),
        value=dates[0]
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

    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(f"Total patients in selected period: {df_selected['Patient_Count'].sum()}")
    st.write("Patients by postal code:")
    st.write(df_selected.sort_values('Patient_Count', ascending=False)) 