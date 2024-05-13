import streamlit as st
import pandas as pd

# Title of the app
st.title('CSV File to DataFrame')

# File uploader allows user to add their own CSV
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    if 'PELKM1' in df.columns:
            # Mapping dictionary for PELKM1
            job_search_methods = {
                "1": "Contacted Employer Directly/Interview",
                "2": "Contacted Public Employment Agency",
                "3": "Contacted Private Employment Agency",
                "4": "Contacted Friends Or Relatives",
                "5": "Contacted School/University Employment Center",
                "6": "Sent Out Resumes/Filled Out Application",
                "7": "Checked Union/Professional Registers",
                "8": "Placed Or Answered Ads",
                "9": "Other Active",
                "10": "Looked At Ads",
                "11": "Attended Job Training Programs/Courses",
                "12": "Nothing",
                "13": "Other Passive"
            }
            df['PELKM1'] = df['PELKM1'].map(job_search_methods)
            test = pd.DataFrame(df['PELKM1'])
            test['count'] =1
            # Perform grouping
            grouped_data =test.groupby('PELKM1').sum()
            grouped_data.rename(columns={
                    'PELKM1 ': 'tee',
                    'Count ': 'Count'
                }, inplace=True)
            # Create a plot using Plotly
            #fig = px.bar(grouped_data, x='PELKM1', y='PELKM1', title='Total Values by Category')
            
            # Display the plot
            st.write(f"### Unemployed looking-search methods", grouped_data)
        elif 'PELKAVL' in df.columns:
            job_search_methods = {
                "1": "Yes",
                "2": "No"
            }
            df['PELKAVL'] = df['PELKAVL'].map(job_search_methods)
            test = pd.DataFrame(df['PELKAVL'])
            test['count'] =1
            # Perform grouping
            #grouped_data =test.groupby('PELKAVL').sum()
            test.groupby('PELKAVL').sum().rename(columns={'PELKAVL': 'test1'})
            # Display the plot
            st.write(f"### Unemployed available for work last week", test)
        elif 'PELKDUR' in df.columns:
            st.write("not ready yet")
        elif 'PELKFTO' in df.columns:
            st.write("not ready yet")
        elif 'PELKLL1O' in df.columns:
            st.write("not ready yet")
        elif 'PLKLL2O' in df.columns:
            st.write("not ready yet")
        elif 'PELKLWO' in df.columns:
            st.write("not ready yet")
        else:
            st.write("Column 'PELKM1' does not exist in DataFrame.")
    else:
            st.write("Received data is empty or malformed.")


