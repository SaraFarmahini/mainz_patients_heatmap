# Patient Distribution Visualization

This Streamlit app visualizes the spatial-temporal distribution of patients in Mainz, Germany.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run spatial_temporal_distribution.py
```

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (spatial_temporal_distribution.py)
6. Click "Deploy"

## Data Requirements

The app requires a CSV file named 'filtered_ICD_english.csv' with the following columns:
- Planned Date
- Postal Code 