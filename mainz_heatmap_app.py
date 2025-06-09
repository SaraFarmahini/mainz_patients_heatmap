import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page config for better performance
st.set_page_config(
    page_title="Mainz Patients Visualization",
    page_icon="🏥",
    layout="wide"
)

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""
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

def password_entered():
    """Checks whether a password entered by the user is correct."""
    if st.session_state["password"] == st.secrets["password"]:
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # Don't store password.
    else:
        st.session_state["password_correct"] = False

if check_password():
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
    
    # Create visualization
    fig = px.bar(
        df_selected,
        x='Postal Code',
        y='Patient_Count',
        title=f'Patient Count by Postal Code - {selected_date.strftime("%B %Y")}',
        labels={'Patient_Count': 'Number of Patients'},
        color='Patient_Count',
        color_continuous_scale='Viridis'
    )
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Display
    st.plotly_chart(fig, use_container_width=True)

    # Summary
    st.write("### Summary")
    st.write(f"Total patients: {df_selected['Patient_Count'].sum():,}")
    st.write("Top 5 postal codes by patient count:")
    st.write(df_selected.nlargest(5, 'Patient_Count')[['Postal Code', 'Patient_Count']]) 