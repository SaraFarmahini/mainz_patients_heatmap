# Mainz Patients Heatmap Visualization

This Streamlit application visualizes the spatial distribution of patients across different postal codes in Mainz, Germany, with an interactive time-based slider to view patient distribution across different months.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Required Files

1. `mainz_heatmap_app.py` - The main application file
2. `postal_codes.py` - Contains postal code coordinates for Mainz
3. `monthly_postal_counts.csv` - Data file containing patient counts by postal code and month
4. `requirements.txt` - List of Python dependencies

## Setup Instructions

1. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment (recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure all required files are in the same directory:
   - `mainz_heatmap_app.py`
   - `postal_codes.py`
   - `monthly_postal_counts.csv`

2. Run the Streamlit app:
```bash
streamlit run mainz_heatmap_app.py
```

3. The application will open in your default web browser at `http://localhost:8501`

## Features

- Interactive map showing patient distribution across Mainz
- Time slider to view patient distribution across different months
- Color-coded visualization based on patient count
- Hover information showing postal code and patient count details

## Data Format

The `monthly_postal_counts.csv` file should contain the following columns:
- Year
- Month
- Postal Code
- Patient_Count

## Troubleshooting

If you encounter any issues:

1. Ensure all required files are present in the correct directory
2. Verify that your Python version is 3.8 or higher
3. Check that all dependencies are correctly installed
4. Make sure the CSV file format matches the expected structure

## Deployment

To deploy this application to Streamlit Cloud:

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (mainz_heatmap_app.py)
6. Click "Deploy" 