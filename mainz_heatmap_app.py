import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Set page config for better performance
st.set_page_config(
    page_title="Mainz Patients Visualization",
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
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_data():
        try:
            # First try to read from the repository
            df = pd.read_csv('monthly_postal_counts.csv')
        except FileNotFoundError:
            # If file not found, use file uploader
            uploaded_file = st.file_uploader("Upload monthly_postal_counts.csv", type=['csv'])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            else:
                st.error("Please upload the data file or ensure it exists in the repository")
                return None
        
        if df is not None:
            df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
        return df

    # Load data with error handling
    df = load_data()
    if df is None:
        st.stop()

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
    
    # Create a bar chart using plotly
    fig = px.bar(
        df_selected,
        x='Postal Code',
        y='Patient_Count',
        title=f'Patient Count by Postal Code - {selected_date.strftime("%B %Y")}',
        labels={'Patient_Count': 'Number of Patients', 'Postal Code': 'Postal Code'},
        color='Patient_Count',
        color_continuous_scale='Viridis'
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Postal Code",
        yaxis_title="Number of Patients",
        showlegend=False
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(f"Total patients in selected period: {df_selected['Patient_Count'].sum()}")
    st.write("Patients by postal code:")
    st.write(df_selected.sort_values('Patient_Count', ascending=False)) 