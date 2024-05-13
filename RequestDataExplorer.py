import streamlit as st
import pandas as pd

# Title of the app
st.title('CSV File to DataFrame')

# File uploader allows user to add their own CSV
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    filtered_df = df.query('PELKAVL > 0')

    # Display the DataFrame
    st.write(filtered_df)

    # Show statistics about the DataFrame if needed
    if st.button('Show Summary'):
        st.write(filtered_df.describe())

